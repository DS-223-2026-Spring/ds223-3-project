"""
Pivot survey into training rows.

Each respondent becomes N rows — one per activity they picked and specified a
style for. A person who picked Yoga + Dance with Hatha + Salsa contributes 2
rows with identical preference features but different style_bucket labels.

This teaches the model that the same personality profile can map to multiple
buckets across activities — exactly the uncertainty `predict_proba` captures.
'activity' is NOT a feature; the model predicts across ALL 9 buckets.
"""
import pandas as pd

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

ACTIVITY_TO_STYLE_COL = {
    "Yoga": "yoga_style",
    "Dance": "dance_style",
    "Fitness": "fitness_style",
}

FEATURE_COLS = ["age", "gender", "experience_level", "group_preference",
                "energy_preference", "structure_preference", "goal"]


def prepare(survey_df: pd.DataFrame) -> pd.DataFrame:
    """Convert wide survey into long (features, style_bucket) training rows."""
    rows = []
    for _, r in survey_df.iterrows():
        interests = [a.strip() for a in str(r["activity_interest"]).split(",")]
        for activity in interests:
            style_col = ACTIVITY_TO_STYLE_COL.get(activity)
            if not style_col or style_col not in r:
                continue
            raw_style = r[style_col]
            if pd.isna(raw_style) or raw_style == "Not sure yet":
                continue
            bucket = STYLE_BUCKETS.get(raw_style)
            if bucket is None:
                continue
            rows.append({
                **{c: r[c] for c in FEATURE_COLS},
                "target_style_bucket": bucket,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "model/data/survey.csv"
    out = sys.argv[2] if len(sys.argv) > 2 else "model/data/training_survey.csv"
    survey = pd.read_csv(src)
    train = prepare(survey)
    print(f"Survey rows: {len(survey)}  →  Training rows: {len(train)}")
    print(train["target_style_bucket"].value_counts())
    train.to_csv(out, index=False)

