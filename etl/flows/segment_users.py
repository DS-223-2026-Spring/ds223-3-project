"""
K-means user segmentation flow.

Wraps the ds/scripts/segment_users.py script in a Prefect flow so it
runs as part of the production pipeline.

Inputs:  ds/data/survey_combined.csv (or survey.csv as fallback)
Outputs: rows in segments table (4 personas)
"""
from prefect import flow, task, get_run_logger
import subprocess


@task(retries=1, retry_delay_seconds=5)
def run_segmentation():
    """Trigger the K-means clustering script."""
    logger = get_run_logger()
    logger.info("Running K-means segmentation...")
    subprocess.run(
        ["python", "-m", "ds.scripts.segment_users"],
        check=True, cwd="/app",
    )


@flow(name="segment-users", log_prints=True)
def segment_users_flow():
    """Cluster respondents into personas and write to segments table."""
    run_segmentation()


if __name__ == "__main__":
    segment_users_flow()