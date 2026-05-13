from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine
from app.routes import quiz, recommend, studios, segments, users, bookings

app = FastAPI(title="ActivityHub Backend")

@app.on_event("startup")
def ensure_schema():
    """Idempotent schema check, creates missing tables on stale volumes."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                class_id INT NOT NULL REFERENCES classes(class_id) ON DELETE CASCADE,
                feedback VARCHAR(50),
                booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id)"))
        
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
