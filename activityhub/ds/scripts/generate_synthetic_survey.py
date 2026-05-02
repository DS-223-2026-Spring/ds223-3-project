"""
Persona-based synthetic survey generator.

Existing `augment_training.py` only adds noise to real rows. This script
generates new respondents from realistic persona templates so each style
bucket gets enough samples for the model to learn confidently.

Output: ds/data/survey_synthetic.csv  (~270 rows)
        Each row tagged data_source='synthetic'.

Usage:
    python -m ds.scripts.generate_synthetic_survey
"""
import os
import numpy as np
import pandas as pd

np.random.seed(42)

OUT_PATH = "ds/data/survey_synthetic.csv"

# Each persona maps to one or more style buckets in the trained model.
# Sampling weights inside lists are uniform.
PERSONAS = {
    "yoga_calm_seeker": {
        "n_rows": 30,
        "age_range": (22, 50),
        "gender": ["female", "female", "female", "male"],
        "experience_level": ["beginner", "intermediate"],
        "group_preference": ["small group", "solo"],
        "energy_preference": ["low energy"],
        "structure_preference": ["structured"],
        "goal": ["stress relief", "flexibility", "mindfulness"],
        "activity_interest": "Yoga",
        "yoga_style": ["Hatha", "Restorative", "Yin"],
        "dance_style": [None],
        "fitness_style": [None],
    },
    "yoga_dynamic": {
        "n_rows": 30,
        "age_range": (20, 40),
        "gender": ["female", "female", "male"],
        "experience_level": ["intermediate", "advanced"],
        "group_preference": ["small group", "large group"],
        "energy_preference": ["moderate energy", "high energy"],
        "structure_preference": ["structured", "free-form"],
        "goal": ["fitness", "flexibility", "stress relief"],
        "activity_interest": "Yoga",
        "yoga_style": ["Vinyasa", "Power"],
        "dance_style": [None],
        "fitness_style": [None],
    },
    "yoga_aerial": {
        "n_rows": 25,
        "age_range": (20, 35),
        "gender": ["female", "female", "female", "male"],
        "experience_level": ["intermediate", "advanced"],
        "group_preference": ["small group"],
        "energy_preference": ["moderate energy", "high energy"],
        "structure_preference": ["structured"],
        "goal": ["fitness", "fun", "flexibility"],
        "activity_interest": "Yoga",
        "yoga_style": ["Aerial"],
        "dance_style": [None],
        "fitness_style": [None],
    },
    "dance_latin": {
        "n_rows": 30,
        "age_range": (22, 45),
        "gender": ["female", "female", "male"],
        "experience_level": ["beginner", "intermediate"],
        "group_preference": ["small group", "large group"],
        "energy_preference": ["moderate energy", "high energy"],
        "structure_preference": ["structured", "free-form"],
        "goal": ["fun", "social", "fitness"],
        "activity_interest": "Dance",
        "yoga_style": [None],
        "dance_style": ["Salsa / latin / ballroom", "Bachata"],
        "fitness_style": [None],
    },
    "dance_urban": {
        "n_rows": 30,
        "age_range": (16, 30),
        "gender": ["female", "male"],
        "experience_level": ["beginner", "intermediate"],
        "group_preference": ["large group", "small group"],
        "energy_preference": ["high energy"],
        "structure_preference": ["free-form", "structured"],
        "goal": ["fun", "social", "fitness"],
        "activity_interest": "Dance",
        "yoga_style": [None],
        "dance_style": ["Hip-hop / street", "Jazz funk"],
        "fitness_style": [None],
    },
    "dance_classical": {
        "n_rows": 30,
        "age_range": (16, 50),
        "gender": ["female", "female", "female", "male"],
        "experience_level": ["beginner", "intermediate", "advanced"],
        "group_preference": ["small group"],
        "energy_preference": ["moderate energy"],
        "structure_preference": ["structured"],
        "goal": ["flexibility", "discipline", "stress relief"],
        "activity_interest": "Dance",
        "yoga_style": [None],
        "dance_style": ["Contemporary / ballet", "Armenian / Joxovrdakan"],
        "fitness_style": [None],
    },
    "fitness_high_intensity": {
        "n_rows": 30,
        "age_range": (20, 40),
        "gender": ["male", "male", "female"],
        "experience_level": ["intermediate", "advanced"],
        "group_preference": ["large group", "solo"],
        "energy_preference": ["high energy"],
        "structure_preference": ["structured", "free-form"],
        "goal": ["fitness", "weight loss"],
        "activity_interest": "Fitness",
        "yoga_style": [None],
        "dance_style": [None],
        "fitness_style": ["HIIT / cardio", "CrossFit"],
    },
    "fitness_strength": {
        "n_rows": 30,
        "age_range": (20, 50),
        "gender": ["male", "male", "female"],
        "experience_level": ["beginner", "intermediate", "advanced"],
        "group_preference": ["solo", "small group"],
        "energy_preference": ["moderate energy", "high energy"],
        "structure_preference": ["structured"],
        "goal": ["fitness", "weight loss", "discipline"],
        "activity_interest": "Fitness",
        "yoga_style": [None],
        "dance_style": [None],
        "fitness_style": ["Strength training", "Functional training", "TRX"],
    },
    "fitness_controlled": {
        "n_rows": 30,
        "age_range": (25, 55),
        "gender": ["female", "female", "female", "male"],
        "experience_level": ["beginner", "intermediate"],
        "group_preference": ["small group", "solo"],
        "energy_preference": ["low energy", "moderate energy"],
        "structure_preference": ["structured"],
        "goal": ["flexibility", "stress relief", "fitness"],
        "activity_interest": "Fitness",
        "yoga_style": [None],
        "dance_style": [None],
        "fitness_style": ["Pilates"],
    },
}

DISTRICTS = ["Kentron", "Arabkir", "Kanaker-Zeytun", "Davtashen",
             "Erebuni", "Avan", "Malatia-Sebastia"]
PREFERRED_TIME = ["morning", "afternoon", "evening"]
MAX_TRAVEL = ["1km", "3km", "5km", "10km", "any"]


def _sample(values):
    """Random pick from list."""
    return values[np.random.randint(len(values))]


def _generate_one(persona: dict) -> dict:
    """Build a single synthetic survey row from a persona template."""
    age_lo, age_hi = persona["age_range"]
    return {
        "age": int(np.random.randint(age_lo, age_hi + 1)),
        "gender": _sample(persona["gender"]),
        "district": _sample(DISTRICTS),
        "activity_interest": persona["activity_interest"],
        "yoga_style": _sample(persona["yoga_style"]),
        "dance_style": _sample(persona["dance_style"]),
        "fitness_style": _sample(persona["fitness_style"]),
        "max_travel_km": _sample(MAX_TRAVEL),
        "group_preference": _sample(persona["group_preference"]),
        "energy_preference": _sample(persona["energy_preference"]),
        "experience_level": _sample(persona["experience_level"]),
        "goal": _sample(persona["goal"]),
        "structure_preference": _sample(persona["structure_preference"]),
        "preferred_time": _sample(PREFERRED_TIME),
        "data_source": "synthetic",
    }


def generate(out_path: str = OUT_PATH) -> int:
    """Generate synthetic rows for all personas. Returns count."""
    rows = []
    for name, p in PERSONAS.items():
        for _ in range(p["n_rows"]):
            rows.append(_generate_one(p))
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return len(df)


def merge_real_and_synthetic(
    real_path: str = "ds/data/survey.csv",
    synth_path: str = OUT_PATH,
    out_path: str = "ds/data/survey_combined.csv",
) -> int:
    """Concatenate real + synthetic surveys for training. Returns total count."""
    real = pd.read_csv(real_path)
    if "data_source" not in real.columns:
        real["data_source"] = "real"
    synth = pd.read_csv(synth_path)
    combined = pd.concat([real, synth], ignore_index=True)
    combined.to_csv(out_path, index=False)
    return len(combined)


if __name__ == "__main__":
    n = generate()
    print(f"Generated {n} synthetic survey rows {OUT_PATH}")
    total = merge_real_and_synthetic()
    print(f"Combined real + synthetic: {total} rows ds/data/survey_combined.csv")
