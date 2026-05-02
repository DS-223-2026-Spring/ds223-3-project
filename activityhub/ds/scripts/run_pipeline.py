"""
End-to-end DS pipeline: generate synthetic → combine → prepare → augment → train.

Triggers everything in order. Safe to re-run as many times as needed —
overwrites intermediate CSVs and the final pkl each time.

Usage:
    python -m ds.scripts.run_pipeline
"""
import subprocess
import pandas as pd

from ds.scripts.prepare_survey import prepare
from ds.scripts.augment_training import augment
from ds.scripts.generate_synthetic_survey import generate, merge_real_and_synthetic


def run():
    """Run all DS steps end-to-end."""
    print("[1/5] Generating persona-based synthetic survey...")
    n_synth = generate()
    print(f"{n_synth} synthetic rows")

    print("[2/5] Combining real + synthetic surveys...")
    n_combined = merge_real_and_synthetic()
    print(f"{n_combined} combined rows")

    print("[3/5] Preparing training rows from combined survey...")
    survey = pd.read_csv("ds/data/survey_combined.csv")
    train_df = prepare(survey)
    train_df.to_csv("ds/data/training_survey.csv", index=False)
    print(f"{len(train_df)} training rows")
    print(train_df["target_style_bucket"].value_counts())

    print("[4/5] Augmenting...")
    augmented = augment(train_df)
    augmented.to_csv("ds/data/training_survey_augmented.csv", index=False)
    print(f"{len(augmented)} augmented rows")

    print("[5/5] Training model...")
    subprocess.run(["python", "-m", "ds.scripts.train_model"], check=True)

    print("\nPipeline complete.")


if __name__ == "__main__":
    run()