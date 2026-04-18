# Data paths
DATA_PATH = "data/"
SURVEY_DATA_FILE = "survey_data.csv"
STUDIO_DATA_FILE = "studio_data.csv"
SYNTHETIC_DATA_FILE = "synthetic_data.csv"

# Model configuration
MODEL_NAME = "recommendation_model"
MODEL_PATH = "models/"

# Training parameters
TRAINING_EPOCHS = 100
BATCH_SIZE = 32
LEARNING_RATE = 0.001

# Scheduling
SCHEDULED_TASKS = {
    "data_ingestion": "daily",
    "model_training": "weekly",
    "recommendation_generation": "daily"
}

# Logging
LOG_FILE_PATH = "logs/orchestration_logs.txt"

# API settings (if applicable)
API_URL = "http://localhost:8000/predict"
API_TIMEOUT = 60  # in seconds