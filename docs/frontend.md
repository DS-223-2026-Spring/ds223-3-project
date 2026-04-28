# Frontend

Streamlit multi-page app at port 8501.

## Pages
- `app.py` — landing page
- `pages/1_Quiz.py` — onboarding quiz
- `pages/2_Recommendations.py` — top-3 matches with match score
- `pages/3_Studio_Dashboard.py` — segment insights

The frontend talks to the backend via the `API_URL` env var (set in compose to `http://api:8000`).