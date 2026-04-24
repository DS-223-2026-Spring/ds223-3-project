from fastapi import FastAPI

from app.routers import quiz, recommend, studios, segments, users

app = FastAPI(title="ActivityHub Backend")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(studios.router, prefix="/studios", tags=["studios"])
app.include_router(segments.router, prefix="/segments", tags=["segments"])


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ActivityHub Backend"}
