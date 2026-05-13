"""
Shared inference module: loads the trained classifier and produces
top-k class recommendations for a user.

Used by api/app/routes/recommend.py.
"""
import os
import joblib
import pandas as pd

MODEL_PATH = os.getenv("MODEL_PATH", "/app/ds/models/style_classifier.pkl")

# Maps a class's `style` field → one of the 9 buckets the model predicts
STYLE_BUCKETS = {
    # Yoga
    "Hatha": "Yoga-Calm",
    "Restorative": "Yoga-Calm",
    "Yin": "Yoga-Calm",
    "Vinyasa": "Yoga-Dynamic",
    "Power": "Yoga-Dynamic",
    "Aerial": "Yoga-Aerial",
    # Dance
    "Salsa / latin / ballroom": "Dance-Latin",
    "Bachata": "Dance-Latin",
    "Hip-hop / street": "Dance-Urban",
    "Jazz funk": "Dance-Urban",
    "Contemporary / ballet": "Dance-Classical",
    "Armenian / Joxovrdakan": "Dance-Classical",
    # Fitness
    "HIIT / cardio": "Fitness-HighIntensity",
    "CrossFit": "Fitness-HighIntensity",
    "Strength training": "Fitness-Strength",
    "Functional training": "Fitness-Strength",
    "TRX": "Fitness-Strength",
    "Pilates": "Fitness-Controlled",
}

FEATURE_COLS = ["age", "gender", "experience_level", "group_preference",
                "energy_preference", "structure_preference", "goal"]

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def recommend_top_k(user: dict, classes_df: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    """
    Score every class against the user's predicted bucket distribution
    and return the top-k.

    Args:
        user: dict with keys age, gender, experience_level, group_preference,
              energy_preference, structure_preference, goal, budget_max_amd, district
        classes_df: DataFrame of all available classes from the DB
        k: number of recommendations to return

    Returns:
        DataFrame of top-k classes with an added 'score' column (0–1).
    """
    model = _get_model()

    # 1. Predict bucket distribution for this user
    X = pd.DataFrame([{c: user.get(c) for c in FEATURE_COLS}])
    probs = model.predict_proba(X)[0]
    classes = model.named_steps["clf"].classes_
    bucket_scores = dict(zip(classes, probs))

    # 2. Score each class by mapping its style → bucket → prob
    df = classes_df.copy()
    df["bucket"] = df["style"].map(STYLE_BUCKETS)
    df["score"] = df["bucket"].map(bucket_scores).fillna(0.0)

    # 3. Hard filter: budget
    budget = user.get("budget_max_amd")
    if budget:
        df = df[
            (df["price_per_session_amd"].isna()) |
            (df["price_per_session_amd"] <= budget)
        ]

    # 4. Soft preference: same district bumps score
    user_district = user.get("district")
    if user_district:
        df.loc[df["district"] == user_district, "score"] += 0.05

    # 5. Soft preference: day match (+0.03 per matching day)
    user_days = user.get("preferred_days")
    if user_days:
        # preferred_days can be a list or comma-joined string from the DB
        if isinstance(user_days, str):
            user_days_list = [d.strip().lower() for d in user_days.split(",")]
        else:
            user_days_list = [d.strip().lower() for d in user_days]

        def count_day_matches(class_day):
            if not class_day or pd.isna(class_day):
                return 0
            class_day_str = str(class_day).lower()
            # Match by checking if any preferred day appears in the class day string
            return sum(1 for d in user_days_list if d in class_day_str)

        df["day_matches"] = df["day"].apply(count_day_matches)
        df["score"] = df["score"] + (df["day_matches"] * 0.03)
        df = df.drop(columns=["day_matches"])

    # 6. Soft preference: time match (+0.03 if class falls in preferred window)
    user_time = user.get("preferred_time")
    if user_time and user_time.lower() != "any":
        time_windows = {
            "morning": (6, 12),
            "afternoon": (12, 17),
            "evening": (17, 23),
        }
        window = time_windows.get(user_time.lower())
        if window:
            def time_in_window(class_time):
                if not class_time or pd.isna(class_time):
                    return False
                try:
                    hour = int(str(class_time).split(":")[0])
                    return window[0] <= hour < window[1]
                except (ValueError, IndexError):
                    return False
            df["time_match"] = df["time"].apply(time_in_window)
            df.loc[df["time_match"], "score"] += 0.03
            df = df.drop(columns=["time_match"])

    # 7. Cap score at 1.0 to satisfy Pydantic schema
    df["score"] = df["score"].clip(upper=1.0)

    # 8. Filter out near-zero matches (below 5%)
    MIN_SCORE = 0.05
    qualifying = df[df["score"] >= MIN_SCORE]

    # 9. Sort & return top-k, but never fewer than 1 if any class survives
    if len(qualifying) >= k:
        result = qualifying.sort_values("score", ascending=False).head(k)
    elif len(qualifying) > 0:
        # Return what we have rather than padding with bad matches
        result = qualifying.sort_values("score", ascending=False)
    else:
        # Last resort: return top-1 from full set so user sees something
        result = df.sort_values("score", ascending=False).head(1)

    return result.reset_index(drop=True)