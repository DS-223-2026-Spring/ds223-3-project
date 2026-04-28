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

    # 5. Sort & return top-k
    df = df.sort_values("score", ascending=False).head(k).reset_index(drop=True)
    return df