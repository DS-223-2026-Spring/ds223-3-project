from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd


def train_model(data):
    """
    Train a Random Forest model on the provided data.

    Args:
        data (DataFrame): The data to train the model on.

    Returns:
        model: The trained model.
    """
    # Split the data into features and labels
    X = data.drop("target", axis=1)  # Replace 'target' with the actual column name
    y = data["target"]

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100)

    # Train the model
    model.fit(X, y)

    # Save the trained model to a file
    with open("models/random_forest_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully")
    return model


if __name__ == "__main__":
    data = pd.read_csv("data/survey_data.csv")
    train_model(data)