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
- POST /bookings/ → 200, returns booking_id ✅ verified working after ETL pipeline run
- POST /bookings/ → 404 "User not found" if user_id doesn't exist ✅ proper error handling
- POST /bookings/ → 404 "Class not found — ETL pipeline may not have run yet" if class_id doesn't exist ✅ proper error handling
- GET /bookings/{user_id} → 200, returns user history ✅

## Users
- GET /users/ → 200
- GET /users/{id} → 200 / 404
- POST /users/ → 200
- DELETE /users/{id} → 200

All response shapes match Pydantic schemas in app/models/schemas.py. Verified via FastAPI auto-validation.

---

## Notes
- All endpoints require the ETL pipeline to have run first for recommendations and bookings to work
- POST /bookings/ previously returned HTTP 500 due to missing bookings table — fixed by resetting the Docker volume
- Backend validates user_id and class_id existence before inserting, returning clear 404 errors instead of 500
