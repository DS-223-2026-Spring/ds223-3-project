import pandas as pd

def load_data(file_path):
    """
    Loads data from a given file path (CSV format).

    Args:
        file_path (str): The path to the CSV file to load.

    Returns:
        DataFrame: The loaded data as a pandas DataFrame.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None


if __name__ == "__main__":
    # Example usage: specify the path to the data file
    file_path = "data/survey_data.csv"
    loaded_data = load_data(file_path)

    if loaded_data is not None:
        # Example: print the first few rows of the loaded data
        print(loaded_data.head())