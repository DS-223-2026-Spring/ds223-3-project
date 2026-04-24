# Prefect flow: run the ML training pipeline.
from prefect import flow, task
import subprocess


@task
def prepare():
    subprocess.run(["python", "/app/model/scripts/prepare_survey.py",
                "model/data/survey.csv", "model/data/training_survey.csv"], check=True)


@task
def augment():
    subprocess.run(["python", "/app/model/scripts/augment_training.py",
                "model/data/training_survey.csv",
                "model/data/training_survey_augmented.csv"], check=True)


@task
def train():
    subprocess.run(["python", "/app/model/scripts/train_model.py"], check=True)


@flow(name="train-model")
def train_flow():
    prepare()
    augment()
    train()


if __name__ == "__main__":
    train_flow()
