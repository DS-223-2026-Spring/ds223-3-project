import sys
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd

from app.database import get_db
from app.models.schemas import (
    RecommendRequest, RecommendResponse, RecommendationResponse,
)

# shared/ is mounted at /app/shared by docker-compose
sys.path.insert(0, "/app/shared")

router = APIRouter()


@router.post("/", response_model=RecommendResponse)
def recommend(body: RecommendRequest, db: Session = Depends(get_db)):
    """Generate top-3 recommendations across all activities for a user."""
    try:
        from recommend import recommend_top_k
    except Exception as e:
        raise HTTPException(503, f"Model not available yet: {e}")

    quiz = db.execute(
        text("""SELECT u.age, u.gender, u.district,
                       q.experience_level, q.group_preference, q.energy_preference,
                       q.structure_preference, q.goal,
                       q.budget_max_amd
                FROM users u
                JOIN quiz_responses q ON u.user_id = q.user_id
                WHERE u.user_id = :uid
                ORDER BY q.submitted_at DESC LIMIT 1"""),
        {"uid": body.user_id},
    ).mappings().first()
    if not quiz:
        raise HTTPException(404, "Quiz not found for user")

    classes_rows = db.execute(text("""
        SELECT c.class_id, c.studio_id, c.studio_name, c.activity_type, c.style,
               c.day, c.time, c.duration_min,
               c.price_per_session_amd, c.experience_required,
               c.group_or_private, c.energy_level, c.structure_level, c.district
        FROM classes c
    """)).mappings().all()
    classes_df = pd.DataFrame([dict(r) for r in classes_rows])

    if classes_df.empty:
        raise HTTPException(503, "No classes loaded yet")

    user = {
        "age": quiz["age"],
        "gender": quiz["gender"],
        "district": quiz["district"],
        "experience_level": quiz["experience_level"],
        "group_preference": quiz["group_preference"],
        "energy_preference": quiz["energy_preference"],
        "structure_preference": quiz["structure_preference"],
        "goal": quiz["goal"],
        "budget_max_amd": quiz["budget_max_amd"],
    }

    top = recommend_top_k(user, classes_df, k=3)

    recs = []
    for i, row in enumerate(top.itertuples(), start=1):
        recs.append(RecommendationResponse(
            class_id=int(row.class_id),
            studio_name=row.studio_name,
            activity_type=row.activity_type,
            style=row.style,
            day=row.day or "",
            time=row.time or "",
            price_amd=int(row.price_per_session_amd) if not pd.isna(row.price_per_session_amd) else 0,
            score=float(row.score),
            rank=i,
        ))

    for rec in recs:
        db.execute(
            text("""INSERT INTO recommendations (user_id, class_id, score, rank)
                    VALUES (:uid, :cid, :score, :rank)"""),
            {"uid": body.user_id, "cid": rec.class_id,
             "score": rec.score, "rank": rec.rank},
        )
    db.commit()

    return RecommendResponse(user_id=body.user_id, recommendations=recs)


@router.get("/{user_id}", response_model=RecommendResponse)
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    """Return the most recent saved recommendations for a user."""
    rows = db.execute(
        text("""SELECT r.class_id, r.score, r.rank,
                       c.studio_name, c.activity_type, c.style, c.day, c.time,
                       c.price_per_session_amd
                FROM recommendations r
                JOIN classes c ON r.class_id = c.class_id
                WHERE r.user_id = :uid
                ORDER BY r.generated_at DESC, r.rank ASC
                LIMIT 3"""),
        {"uid": user_id},
    ).mappings().all()

    if not rows:
        raise HTTPException(404, "No recommendations found for user")

    recs = [RecommendationResponse(
        class_id=int(r["class_id"]),
        studio_name=r["studio_name"],
        activity_type=r["activity_type"],
        style=r["style"],
        day=r["day"] or "",
        time=r["time"] or "",
        price_amd=int(r["price_per_session_amd"]) if r["price_per_session_amd"] else 0,
        score=float(r["score"]),
        rank=int(r["rank"]),
    ) for r in rows]

    return RecommendResponse(user_id=user_id, recommendations=recs)