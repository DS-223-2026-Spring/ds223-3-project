import pandas as pd


def validate_data(data):
    """
    Validates the loaded data (check for missing values, duplicates).

    Args:
        data (DataFrame): The data to validate.

    Returns:
        DataFrame: The validated data.
    """
    if data.isnull().sum().any():
        print("Warning: Data contains missing values")

    if data.duplicated().any():
        print("Warning: Data contains duplicate entries")

    # Example of validation: check column names
    required_columns = ['user_id', 'age', 'preference']
    for col in required_columns:
        if col not in data.columns:
            print(f"Missing required column: {col}")

    print("Data validated successfully")
    return data


if __name__ == "__main__":
    # Load sample data for validation
    data = pd.read_csv("data/survey_data.csv")
    validated_data = validate_data(data)
    print(validated_data.head())