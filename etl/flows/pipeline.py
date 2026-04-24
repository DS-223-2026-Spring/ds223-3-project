from prefect import flow
from etl.flows.validate_data import validate_flow
from etl.flows.load_data import load_data_flow
from etl.flows.train_model import train_flow

@flow(name="activityhub-pipeline")
def full_pipeline():
    validate_flow()
    load_data_flow()
    train_flow()


if __name__ == "__main__":
    full_pipeline()