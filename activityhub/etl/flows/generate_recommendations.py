import pickle
import pandas as pd


def generate_recommendations(user_data):
    """
    Generate recommendations based on the trained model.

    Args:
        user_data (DataFrame): The data to generate recommendations for.

    Returns:
        recommendations: The generated recommendations.
    """
    # Load the trained model
    with open("models/random_forest_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Predict the recommendations
    recommendations = model.predict(user_data)
    print("Generated recommendations:", recommendations)
    return recommendations


if __name__ == "__main__":
    # Example user data (replace with actual data)
    user_data = pd.DataFrame([[5, 3, 8]])  # Replace with real input data
    generate_recommendations(user_data)