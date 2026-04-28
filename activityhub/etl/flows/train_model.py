# Prefect flow: run the ML training pipeline.
from prefect import flow, task
import subprocess


@task
def prepare():
    subprocess.run(["python", "/app/ds/scripts/prepare_survey.py",
                "ds/data/survey.csv", "ds/data/training_survey.csv"], check=True)


@task
def augment():
    subprocess.run(["python", "/app/ds/scripts/augment_training.py",
                "ds/data/training_survey.csv",
                "ds/data/training_survey_augmented.csv"], check=True)


@task
def train():
    subprocess.run(["python", "/app/ds/scripts/train_model.py"], check=True)


@flow(name="train-model")
def train_flow():
    prepare()
    augment()
    train()


if __name__ == "__main__":
    train_flow()
