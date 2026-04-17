# ActivityHub Backend

A FastAPI service powering ActivityHub — a personalized activity matching platform that connects users in Yerevan with extracurricular studios based on their preferences, schedule, and budget.

---

## How to Run

From the project root:

```bash
docker compose up --build
```

| | URL |
|---|---|
| API base | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |

---

## API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/quiz/` | Submit a user preference quiz |
| GET | `/quiz/{user_id}` | Get quiz answers for a user |
| PUT | `/quiz/{user_id}` | Update quiz answers for a user |
| DELETE | `/quiz/{user_id}` | Delete quiz answers for a user |
| GET | `/studios/` | List all studios |
| GET | `/studios/{studio_id}` | Get a single studio |
| POST | `/studios/` | Create a new studio |
| PUT | `/studios/{studio_id}` | Update a studio |
| DELETE | `/studios/{studio_id}` | Delete a studio |
| POST | `/recommend/` | Get activity recommendations for a user |
| GET | `/recommend/{user_id}` | Get saved recommendations for a user |
| GET | `/segments/` | List all user segments |
| GET | `/segments/{segment_id}` | Get a single segment |
| POST | `/segments/` | Create a new segment |
| DELETE | `/segments/{segment_id}` | Delete a segment |

---

## API Assumptions

- All endpoints currently return **dummy/hardcoded data** — no real database is connected yet
- User IDs are integers starting from 1
- Prices are in **AMD (Armenian Dram)**
- All studio locations are within **Yerevan**
- Match scores are floats between **0 and 1** (higher = better match)
- Experience levels are: `beginner`, `intermediate`, `advanced`

---

## Pending Dependencies

| Dependency | Blocking |
|---|---|
| **DB Developer** | PostgreSQL schema and tables must be ready before dummy data can be replaced with real queries |
| **Data Scientist** | Trained ML model (`.pkl` file) needed to power the `/recommend` endpoint |
| **Frontend Developer** | Endpoint contracts should be confirmed before the Streamlit app connects to this API |
| **Environment** | `.env` file with real DB credentials must be created before connecting to PostgreSQL |

---

## Tech Stack

| Component | Status |
|---|---|
| FastAPI | Active |
| Python 3.11 | Active |
| Docker | Active |
| PostgreSQL | Pending |
| scikit-learn | Pending (recommendation model) |
