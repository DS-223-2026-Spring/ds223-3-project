# Visual Analytics Integration Guide

How analytics and model outputs flow from DS → Backend → Frontend.

## Overview

ActivityHub exposes three categories of model output as visual analytics:

1. **Per-user recommendations** — top-3 class matches with confidence scores
2. **User segments** — K-means personas with size + booking likelihood
3. **Model performance** — Top-1/Top-3 accuracy by model variant

Each category has a defined data path: DS computes → DB stores → Backend serves → Frontend renders.

## 1. Recommendations + Match Scores

**DS owns**: `shared/recommend.py` exposes `recommend_top_k(user, classes_df, k)` which loads the trained pkl and returns scored classes.

**DB stores**: `recommendations` table — rows per (user_id, class_id, score, rank, generated_at).

**Backend serves**: 
- `POST /recommend/` — generates fresh recommendations, writes to DB, returns response
- `GET /recommend/{user_id}` — reads most recent recommendations for a user

**Frontend renders**: `app/pages/2_Recommendations.py`
- Each recommendation as `st.container(border=True)` card
- Match % via `st.metric(label="Match", value=f"{pct}%")`
- "I tried this" button → POST `/bookings/` (feeds back into next retraining)

## 2. User Segments

**DS owns**: `ds/scripts/segment_users.py` runs K-means on quiz_responses, writes 4 personas to DB.

**DB stores**: `segments` table — segment_id, segment_name, description, size, booking_likelihood.

**Backend serves**: `GET /segments/` — returns all personas ordered by size.

**Frontend renders**: `app/pages/3_Studio_Dashboard.py`
- KPIs: total matched users, avg booking likelihood, segment count → `st.metric`
- Bar chart of segment sizes → `st.bar_chart`
- Filterable segment table → `st.dataframe` + `st.multiselect`

## 3. Model Performance

**DS owns**: `ds/scripts/train_model.py` writes `ds/models/metrics.csv` with Top-1/Top-3 per model variant.

**Distribution**: a copy lives at `docs/model_metrics.csv` so it's accessible via the published mkdocs site.

**Frontend renders**: not currently shown to end users (internal metric). Available for grading reviewers via the docs site.

## Component Constraints

| Component | Constraint |
|-----------|------------|
| Frontend | Built-in Streamlit only — `st.metric`, `st.bar_chart`, `st.dataframe`. No HTML, plotly, custom CSS. |
| Backend | Returns Pydantic-validated JSON. No HTML, no charts. |
| DS | Outputs land in DB tables or CSVs in `ds/models/`. No direct service calls. |

## Data Flow Diagram

```text
User quiz
↓
POST /quiz/    ──── writes quiz_responses ────► DB
│
│ (later)
↓
K-means ◄── ds.scripts.segment_users
│
▼
segments table
│
│
┌───────────────────────────────────┘
│
▼
GET /segments/
│
▼
Studio Dashboard (bar chart + KPI + table)
User clicks "Get Recommendations"
↓
POST /recommend/  ─── reads quiz + classes ──► shared.recommend.recommend_top_k
│                                                  │
│                                                  ▼
│                                          top-3 with scores
│                                                  │
│             writes to recommendations ◄──────────┘
│
▼
Recommendations page (3 cards + match% via st.metric)
│
▼ user clicks "I tried this"
│
POST /bookings/   ──── writes bookings ──► DB
│
│ (feeds future retraining)
▼
```

## Adding a New Visual

To add a new chart or analytic:

1. **DS**: write the producer script. Either store output in a new DB table (preferred) or write a CSV under `ds/models/`.
2. **DB**: add the table to `init.sql` and the allowlist in `crud.py`.
3. **Backend**: add a new route returning the data as JSON. Document in `docs/api-spec.md`.
4. **Frontend**: consume via `requests.get(f"{API_URL}/your-endpoint")`. Render with built-in Streamlit components only.

Tag each PR with the relevant role label so M3/M4 issue tracking stays clean.

## Contacts

| Role | Owner | Branch |
|------|-------|--------|
| DS | Meline | `ds` |
| DB | Liana | `db` |
| Backend | Ani | `back` |
| Frontend | Maria | `front` |
| Orchestration | Hmayak | `orch` |
| PM (this doc) | Anna | `main` |