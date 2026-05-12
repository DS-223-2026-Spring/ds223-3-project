# API Endpoint Test Results

All endpoints tested manually via Swagger UI at http://localhost:8000/docs.

## Health
- GET / → 200 {"status": "ok"}

## Quiz
- POST /quiz/ → 200, returns user_id
- GET /quiz/{user_id} → 200, returns quiz dict
- PUT /quiz/{user_id} → 200, updates
- DELETE /quiz/{user_id} → 200 / 404 if not found

## Recommend
- POST /recommend/ → 200, returns 3 recommendations
- GET /recommend/{user_id} → 200, returns saved recs

## Studios
- GET /studios/ → 200, returns 23 studios
- GET /studios/{id} → 200 / 404
- POST /studios/ → 200, returns new studio_id
- PUT /studios/{id} → 200, updates
- DELETE /studios/{id} → 200

## Segments
- GET /segments/ → 200, returns 4 personas
- GET /segments/{id} → 200 / 404

## Bookings
- POST /bookings/ → 200, returns booking_id
- GET /bookings/{user_id} → 200, returns user history

## Users
- GET /users/ → 200
- GET /users/{id} → 200 / 404
- POST /users/ → 200
- DELETE /users/{id} → 200

All response shapes match Pydantic schemas in app/models/schemas.py. Verified via FastAPI auto-validation.
