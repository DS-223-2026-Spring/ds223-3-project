# Frontend
# ActivityHub Frontend

Streamlit multi-page app.

## Pages
- app.py — landing page
- pages/1_Quiz.py — onboarding quiz, POSTs to /quiz/
- pages/2_Recommendations.py — displays top-3 matches from /recommend/
- pages/3_Studio_Dashboard.py — shows segments from /segments/

## API contracts (expected response shapes)
- POST /quiz/ → { user_id: int, message: str }
- POST /recommend/ → { user_id, recommendations: [{class_id, studio_name, activity_type, style, day, time, price_amd, score, rank}] }
- GET /segments/ → [{segment_id, segment_name, description, size, booking_likelihood}]

## Run locally
`bash
streamlit run app.py