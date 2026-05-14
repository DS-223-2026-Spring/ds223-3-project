# Frontend

Streamlit multi-page app at port 8501.

## Pages
- `app.py` — landing page
- `pages/1_Quiz.py` — onboarding quiz
- `pages/2_Recommendations.py` — top-3 matches with match score
- `pages/3_Studio_Dashboard.py` — segment insights

The frontend talks to the backend via the `API_URL` env var (set in compose to `http://api:8000`).

# Frontend Component Specification

Each Streamlit page below uses **only built-in components**

---

## Page 1: Quiz (`pages/1_Quiz.py`)

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

## Page 2: Recommendations (`pages/2_Recommendations.py`)

| Element                | Component               | Notes                            |
|------------------------|-------------------------|----------------------------------|
| Mix summary            | `st.markdown`           | "Your mix: Yoga · Dance"         |
| Recommendation card    | `st.container(border=True)` | one per recommendation       |
| Match %                | `st.metric`             | replace HTML with native widget  |
| "I tried this" button  | `st.button`             | POSTs to /bookings/              |
| Retake quiz            | `st.button`             | navigates to page 1              |

---

## Page 3: Studio Dashboard (`pages/3_Studio_Dashboard.py`)

| Element                | Component               | Notes                            |
|------------------------|-------------------------|----------------------------------|
| Segment counts chart   | `st.bar_chart`          | data from GET /segments/         |
| Top studios            | `st.dataframe`          | filterable                       |
| Booking likelihood KPI | `st.metric`             | per segment                      |
| Filter by activity     | `st.selectbox`          | yoga/dance/fitness/all           |

---