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

# Frontend Component Specification

Each Streamlit page below uses **only built-in components** per issue #90.

---

## Page 1 — Quiz (`pages/1_Quiz.py`)

| Field                  | Component                | Notes                          |
|------------------------|--------------------------|--------------------------------|
| Age                    | `st.number_input`        | min=10, max=100                |
| Gender                 | `st.selectbox`           | M/F/Other                      |
| District               | `st.selectbox`           | from list of Yerevan districts |
| Experience level       | `st.radio`               | beginner/intermediate/advanced |
| Group preference       | `st.radio`               | solo/small/large               |
| Energy preference      | `st.radio`               | low/moderate/high              |
| Structure preference   | `st.radio`               | structured/free-form           |
| Goal                   | `st.selectbox`           | stress-relief/fitness/social/etc |
| Budget                 | `st.slider`              | 0–50000 AMD step 1000          |
| Preferred days         | `st.multiselect`         | days of week                   |
| Preferred time         | `st.radio`               | morning/afternoon/evening      |
| Max travel             | `st.selectbox`           | 1km/3km/5km/10km/any           |
| Submit                 | `st.button`              | calls POST /quiz/              |

---

## Page 2 — Recommendations (`pages/2_Recommendations.py`)

| Element                | Component               | Notes                            |
|------------------------|-------------------------|----------------------------------|
| Mix summary            | `st.markdown`           | "Your mix: Yoga · Dance"         |
| Recommendation card    | `st.container(border=True)` | one per recommendation       |
| Match %                | `st.metric`             | replace HTML with native widget  |
| "I tried this" button  | `st.button`             | POSTs to /bookings/              |
| Retake quiz            | `st.button`             | navigates to page 1              |

---

## Page 3 — Studio Dashboard (`pages/3_Studio_Dashboard.py`)

| Element                | Component               | Notes                            |
|------------------------|-------------------------|----------------------------------|
| Segment counts chart   | `st.bar_chart`          | data from GET /segments/         |
| Top studios            | `st.dataframe`          | filterable                       |
| Booking likelihood KPI | `st.metric`             | per segment                      |
| Filter by activity     | `st.selectbox`          | yoga/dance/fitness/all           |

---

## What's removed 

- HTML strings inside `st.markdown(unsafe_allow_html=True)` for match % rendering — replaced with `st.metric`
- Custom CSS — none, only Streamlit defaults

# Data Flow Architecture

How data moves between roles and services.

User
↓ (fills quiz in browser)
Frontend (Streamlit)
↓ POST /quiz/
Backend (FastAPI)
↓ INSERT users, quiz_responses
Postgres (DB)
User
↓ (clicks "Get Recommendations")
Frontend
↓ POST /recommend/ {user_id}
Backend
↓ SELECT quiz, classes
Postgres
↓ (returns rows)
Backend
↓ calls shared.recommend.recommend_top_k(user, classes, k=3)
Shared inference module
↓ loads /app/ds/models/style_classifier.pkl
↓ returns ranked classes
Backend
↓ INSERT recommendations
Postgres
↓ returns response
Frontend (renders cards)
User clicks "I tried this"
↓ POST /bookings/
Backend
↓ INSERT bookings
Postgres
ETL (daily, scheduled by Prefect)
↓ pulls fresh quiz_responses + bookings + survey_responses
↓ runs prepare → augment → train
↓ writes new style_classifier.pkl
DS pipeline

## Role responsibilities

| Role           | Owns                                       | Depends on                       |
|----------------|--------------------------------------------|----------------------------------|
| DB (Liana)     | init.sql, crud.py, connection.py, schemas  | PM endpoint spec                 |
| DS (Meline)    | model training, K-means, recommend_top_k   | DB tables, ETL pipeline trigger  |
| Backend (Ani)  | FastAPI routes, request/response schemas   | DB CRUD, DS inference function   |
| Frontend (Maria) | Streamlit pages, user-facing flow        | Backend endpoints, frontend spec |
| Orch (Hmayak)  | Prefect flows, scheduling, retraining      | DS scripts, DB connection        |
| PM (Anna)      | Specs, alignment, blockers, integration    | All                              |

## Key contracts

1. **`/recommend/` request shape** is fixed — `{ user_id: int }`. Frontend can't deviate; Backend can't add required fields.
2. **`recommend_top_k(user, classes_df, k)` signature** — DS owns this; Backend imports it; both must keep it stable.
3. **`segments` table schema** — DS writes K-means output here; Backend exposes via `/segments/`; Frontend renders.
4. **`bookings` table** — Backend writes on POST `/bookings/`; ETL reads as feature for retraining.
5. **Model file path** — `/app/ds/models/style_classifier.pkl` — agreed by DS + Backend, must not move.

## Failure-mode contracts

If a service is down, others should fail gracefully:
- Frontend without Backend → show "Service unavailable" not blank page
- Backend without DB → return 503 not 500
- Backend without model pkl → return 503 with "model not loaded"
- ETL without DB → fail flow, log error, exit non-zero