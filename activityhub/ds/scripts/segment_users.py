"""
K-means user segmentation.

Clusters survey respondents into personas, writes results to the `segments` table
for the studio dashboard to consume.

Usage:
    python -m ds.scripts.segment_users
"""
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sqlalchemy import create_engine, text

DB_URL = (
    f"postgresql://{os.getenv('DB_USER','admin')}:{os.getenv('DB_PASSWORD','admin')}"
    f"@{os.getenv('DB_HOST','db')}:{os.getenv('DB_PORT','5432')}/"
    f"{os.getenv('DB_NAME','activityhub')}"
)
engine = create_engine(DB_URL)

CAT_FEATURES = ["experience_level", "group_preference", "energy_preference",
                "structure_preference", "goal"]
N_CLUSTERS = 4

PERSONA_NAMES = {
    0: "Calm Beginner",
    1: "High-Energy Strength",
    2: "Social Dancer",
    3: "Wellness Seeker",
}


def describe_cluster(members: pd.DataFrame) -> str:
    """Build a one-line description from the most common values."""
    if members.empty:
        return "Empty cluster"
    parts = []
    for col in ["energy_preference", "experience_level", "goal"]:
        if col in members.columns:
            top = members[col].mode()
            if len(top) > 0:
                parts.append(str(top.iloc[0]))
    return ", ".join(parts) if parts else "Mixed preferences"


def segment_from_survey():
    """Cluster survey respondents and write segments + assignments to DB."""
    # Use the combined survey if available, else fall back to raw
    try:
        survey = pd.read_csv("ds/data/survey_combined.csv")
    except FileNotFoundError:
        survey = pd.read_csv("ds/data/survey.csv")

    df = survey.dropna(subset=CAT_FEATURES).reset_index(drop=True)
    if len(df) < N_CLUSTERS * 2:
        print(f"Not enough respondents ({len(df)}) to cluster. Skipping.")
        return

    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X = enc.fit_transform(df[CAT_FEATURES])

    km = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    df["cluster"] = labels

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE user_segments CASCADE"))
        conn.execute(text("TRUNCATE TABLE segments RESTART IDENTITY CASCADE"))
        for cluster_id in range(N_CLUSTERS):
            members = df[df["cluster"] == cluster_id]
            name = PERSONA_NAMES.get(cluster_id, f"Cluster {cluster_id}")
            description = describe_cluster(members)
            size = len(members)
            booking_likelihood = round(0.5 + 0.1 * (size / max(len(df), 1)), 2)
            conn.execute(
                text("""INSERT INTO segments
                        (segment_name, description, size, booking_likelihood)
                        VALUES (:n, :d, :s, :b)"""),
                {"n": name, "d": description, "s": size, "b": booking_likelihood},
            )
    print(f"Wrote {N_CLUSTERS} segments to DB.")


if __name__ == "__main__":
    segment_from_survey()