"""
Light augmentation. For each row create `factor` near-twins with small
categorical noise. Survey already has 400 rows, so factor=2 is enough.
"""
import pandas as pd
import numpy as np

np.random.seed(42)

CAT_COLS = ["gender", "experience_level", "group_preference",
            "energy_preference", "structure_preference", "goal"]


def augment(df: pd.DataFrame, factor: int = 2, flip_prob: float = 0.10) -> pd.DataFrame:
    if len(df) == 0:
        return df
    augmented = [df.copy()]
    for _ in range(factor):
        copy = df.copy()
        for col in CAT_COLS:
            if col not in copy.columns:
                continue
            mask = np.random.rand(len(copy)) < flip_prob
            vals = df[col].dropna().unique()
            if len(vals) > 1:
                copy.loc[mask, col] = np.random.choice(vals, mask.sum())
        if "age" in copy.columns:
            copy["age"] = (copy["age"] + np.random.randint(-2, 3, len(copy))).clip(15, 80)
        augmented.append(copy)
    return pd.concat(augmented, ignore_index=True)


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "data/training_survey.csv"
    out = sys.argv[2] if len(sys.argv) > 2 else "data/training_survey_augmented.csv"
    orig = pd.read_csv(src)
    aug = augment(orig)
    print(f"Original: {len(orig)} | Augmented: {len(aug)}")
    aug.to_csv(out, index=False)
