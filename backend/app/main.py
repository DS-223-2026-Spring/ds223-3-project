from fastapi import FastAPI

from app.routers import quiz, recommend, studios, segments, users
app.include_router(users.router, prefix="/users")

app = FastAPI(title="ActivityHub Backend")

app.include_router(users.router, prefix="/users")
app.include_router(recommend.router, prefix="/recommend")
app.include_router(studios.router, prefix="/studios")
app.include_router(segments.router, prefix="/segments")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ActivityHub Backend"}
