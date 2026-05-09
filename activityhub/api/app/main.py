from fastapi import FastAPI

from app.routes import quiz, recommend, studios, segments, users, bookings

app = FastAPI(title="ActivityHub Backend")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(studios.router, prefix="/studios", tags=["studios"])
app.include_router(segments.router, prefix="/segments", tags=["segments"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])


@app.get("/", summary="Health check")
def health_check():
    """
    Returns {"status": "ok", "service": "ActivityHub Backend"} if the service is running.
    Use this endpoint to verify the backend is reachable before making other API calls.
    """
    return {"status": "ok", "service": "ActivityHub Backend"}
