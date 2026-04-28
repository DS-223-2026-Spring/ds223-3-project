# API

FastAPI service at port 8000. Swagger docs at http://localhost:8000/docs.

## Endpoints
- `POST /quiz/` — submit user quiz, returns user_id
- `GET /quiz/{user_id}` — fetch latest quiz
- `POST /recommend/` — get top-3 class matches
- `GET /studios/` — list all studios
- `GET /segments/` — list user personas
