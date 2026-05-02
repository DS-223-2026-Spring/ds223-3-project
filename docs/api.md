# ActivityHub - API Specification

Authoritative list of all API endpoints, their request/response shapes, and which product feature each one supports.

Base URL: `http://localhost:8000` (Docker), `http://api:8000` (inside Docker network)
OpenAPI docs: `http://localhost:8000/docs`

## Resource - Feature mapping

| Resource    | Endpoints                              | Product feature                          |
|-------------|----------------------------------------|------------------------------------------|
| /quiz       | POST, GET /{user_id}                   | User onboarding flow                     |
| /recommend  | POST, GET /{user_id}                   | Top-3 class recommendations              |
| /studios    | GET, GET /{id}, POST                   | Studio listing                           |
| /classes    | GET, GET /{id}                         | Browse all classes (Studio Dashboard)    |
| /segments   | GET                                    | User personas (Studio Dashboard)         |
| /bookings   | POST                                   | Feedback loop ("I tried this class")     |
| /users      | GET, GET /{id}, POST                   | Internal admin                           |
| /survey     | POST                                   | Add real survey response (M3 retraining) |

---

## /quiz

### `POST /quiz/`
Submit user quiz answers. Creates a new user row + quiz_responses row, returns `user_id`.

**Request:**
```json
{
  "age": 22,
  "gender": "female",
  "district": "Kentron",
  "experience_level": "beginner",
  "group_preference": "small group",
  "energy_preference": "low energy",
  "structure_preference": "structured",
  "goal": "stress relief",
  "budget_max_amd": 15000,
  "preferred_days": ["Monday", "Wednesday"],
  "preferred_time": "evening",
  "max_travel_km": "5km"
}
```

**Response (200):**
```json
{
  "user_id": 42,
  "message": "Quiz submitted successfully"
}
```

### `GET /quiz/{user_id}`
Fetch the most recent quiz for a user.

**Response (200):** same shape as request body, plus `submitted_at` timestamp.

---

## /recommend

### `POST /recommend/`
Generate top-3 recommendations for a user based on their quiz.

**Request:**
```json
{ "user_id": 42 }
```

**Response (200):**
```json
{
  "user_id": 42,
  "recommendations": [
    {
      "class_id": 17,
      "studio_name": "Akhtanak Yoga",
      "activity_type": "yoga",
      "style": "Hatha",
      "day": "Wednesday",
      "time": "18:00",
      "price_amd": 12000,
      "score": 0.31,
      "rank": 1
    }
  ]
}
```

### `GET /recommend/{user_id}`
Return saved recommendation history for a user (latest 10).

---

## /classes

### `GET /classes/`
List all classes. Optional query params: `activity_type`, `studio_id`, `district`.

**Response (200):**
```json
[
  {
    "class_id": 17,
    "studio_id": 3,
    "studio_name": "Akhtanak Yoga",
    "activity_type": "yoga",
    "style": "Hatha",
    "day": "Wednesday",
    "time": "18:00",
    "price_per_session_amd": 12000,
    "price_monthly_amd": null,
    "experience_required": "any",
    "group_or_private": "group",
    "energy_level": "low",
    "structure_level": "structured",
    "district": "Kentron"
  }
]
```

### `GET /classes/{class_id}`
Fetch one class.

---

## /studios

### `GET /studios/`
List all studios.

### `GET /studios/{studio_id}`
Fetch one studio.

### `POST /studios/`
Add a studio. Used by data loading.

**Request:**
```json
{
  "studio_name": "New Yoga",
  "district": "Kentron",
  "address": "12 Sayat Nova",
  "instagram": "@newyoga",
  "price_tier": "mid",
  "studio_type": "yoga"
}
```

---

## /segments

### `GET /segments/`
List user segments (personas) computed by K-means on quiz_responses.

**Response (200):**
```json
[
  {
    "segment_id": 1,
    "segment_name": "Calm Yoga Beginner",
    "description": "Low energy, beginner experience, prefers structured classes",
    "size": 47,
    "booking_likelihood": 0.62
  }
]
```

---

## /bookings

### `POST /bookings/`
Log when a user tries a recommended class. Used as positive signal for next training round.

**Request:**
```json
{
  "user_id": 42,
  "class_id": 17,
  "feedback": "loved it"
}
```

**Response (200):**
```json
{ "booking_id": 99, "message": "Feedback recorded" }
```

---

## /survey

### `POST /survey/`
Add a new survey response (used when a real user fills out the form). Triggers data flow into `survey_responses` table.

**Request:** same shape as `/quiz/` POST plus `yoga_style`, `dance_style`, `fitness_style` if applicable.

---

## /users

Internal endpoints. CRUD for users table.
- `GET /users/`
- `GET /users/{user_id}`
- `POST /users/`

---

## Error responses

All endpoints return:
- `400` — invalid request body (Pydantic validation)
- `404` — resource not found
- `503` — model not loaded (recommend endpoint only)
- `500` — server error (logged, generic message returned)

---

## Authentication

None. All endpoints public. Auth out of scope.
