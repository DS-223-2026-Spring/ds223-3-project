import sys
import os
from prefect import flow

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flows.validate_data import validate_flow
from flows.load_data import load_data_flow
from flows.train_model import train_flow

@flow(name="activityhub-pipeline")
def full_pipeline():
    validate_flow()
    load_data_flow()
    train_flow()


if __name__ == "__main__":
    full_pipeline()