from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import QuizRequest, QuizResponse

router = APIRouter()


@router.post("/", response_model=QuizResponse, summary="Submit onboarding quiz")
def submit_quiz(body: QuizRequest, db: Session = Depends(get_db)):
    """
    Accepts quiz answers: age, gender, district, experience_level, group_preference, energy_preference, structure_preference, goal, budget_max_amd, preferred_days (list of strings), preferred_time, and max_travel_km.
    Creates a new ActivityHub user and stores their onboarding preferences in one step.
    Returns user_id — the frontend must save this value to call the recommend endpoint next.
    """
    user_row = db.execute(
        text("""INSERT INTO users (age, gender, district, data_source)
                VALUES (:age, :gender, :district, 'real')
                RETURNING user_id"""),
        {"age": body.age, "gender": body.gender, "district": body.district},
    ).first()
    user_id = user_row[0]
    db.execute(
        text("""INSERT INTO quiz_responses (
                    user_id, experience_level, group_preference, energy_preference,
                    structure_preference, goal,
                    budget_max_amd, preferred_days, preferred_time, max_travel_km)
                VALUES (:uid, :exp, :gp, :ep, :sp, :goal,
                        :budget, :days, :time, :travel)"""),
        {
            "uid": user_id,
            "exp": body.experience_level,
            "gp": body.group_preference,
            "ep": body.energy_preference,
            "sp": body.structure_preference,
            "goal": body.goal,
            "budget": body.budget_max_amd,
            "days": ",".join(body.preferred_days) if body.preferred_days else None,
            "time": body.preferred_time,
            "travel": body.max_travel_km,
        },
    )
    db.commit()
    return QuizResponse(user_id=user_id, message="Quiz submitted successfully")


@router.get("/{user_id}", summary="Get quiz by user ID")
def get_quiz(user_id: int, db: Session = Depends(get_db)):
    """
    Accepts user_id as a path parameter and returns the user's most recent quiz submission as a flat object.
    The response combines demographics (age, gender, district) with all preference fields: experience_level, group_preference, energy_preference, structure_preference, goal, budget_max_amd, preferred_days, preferred_time, max_travel_km, and submitted_at.
    Returns 404 if no quiz has been submitted for this user.
    """
    row = db.execute(
        text("""SELECT u.user_id, u.age, u.gender, u.district, u.data_source,
                       q.experience_level, q.group_preference, q.energy_preference,
                       q.structure_preference, q.goal,
                       q.budget_max_amd, q.preferred_days, q.preferred_time,
                       q.max_travel_km, q.submitted_at
                FROM users u
                JOIN quiz_responses q ON u.user_id = q.user_id
                WHERE u.user_id = :uid
                ORDER BY q.submitted_at DESC LIMIT 1"""),
        {"uid": user_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Quiz not found for user")
    return dict(row)


@router.put("/{user_id}", response_model=QuizResponse, summary="Update user quiz")
def update_quiz(user_id: int, body: QuizRequest, db: Session = Depends(get_db)):
    """
    Accepts user_id as a path parameter and a full quiz body (same fields as POST /quiz), then inserts a new quiz_responses row making it the active preference profile for class matching.
    After updating, call POST /recommend to regenerate recommendations with the new preferences.
    Returns 404 if the user does not exist.
    """
    user = db.execute(
        text("SELECT user_id FROM users WHERE user_id = :uid"),
        {"uid": user_id},
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.execute(
        text("""INSERT INTO quiz_responses (
                    user_id, experience_level, group_preference, energy_preference,
                    structure_preference, goal,
                    budget_max_amd, preferred_days, preferred_time, max_travel_km)
                VALUES (:uid, :exp, :gp, :ep, :sp, :goal,
                        :budget, :days, :time, :travel)"""),
        {
            "uid": user_id,
            "exp": body.experience_level,
            "gp": body.group_preference,
            "ep": body.energy_preference,
            "sp": body.structure_preference,
            "goal": body.goal,
            "budget": body.budget_max_amd,
            "days": ",".join(body.preferred_days) if body.preferred_days else None,
            "time": body.preferred_time,
            "travel": body.max_travel_km,
        },
    )
    db.commit()
    return QuizResponse(user_id=user_id, message="Quiz updated successfully")


@router.delete("/{user_id}", summary="Delete user and quiz")
def delete_quiz(user_id: int, db: Session = Depends(get_db)):
    """
    Accepts user_id as a path parameter and permanently deletes the user along with all quiz responses, recommendations, and bookings.
    Returns 404 if the user does not exist. This action is irreversible.
    """
    result = db.execute(
        text("DELETE FROM users WHERE user_id = :uid"),
        {"uid": user_id},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User and quiz history deleted successfully"}
