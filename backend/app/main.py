from fastapi import FastAPI

app = FastAPI(title="ActivityHub Backend")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ActivityHub Backend"}
