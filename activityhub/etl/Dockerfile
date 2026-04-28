FROM python:3.11-slim
WORKDIR /app

ENV PREFECT_HOME=/tmp/prefect
ENV PREFECT_SERVER_EPHEMERAL_STARTUP_TIMEOUT_SECONDS=120
ENV PREFECT_LOGGING_LEVEL=INFO

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "flows/pipeline.py"]