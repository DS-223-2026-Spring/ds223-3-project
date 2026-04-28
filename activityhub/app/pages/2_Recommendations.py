
import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://api:8000")

ACTIVITY_EMOJI = {"yoga": "🧘", "dance": "💃", "fitness": "💪"}

st.set_page_config(page_title="Your Matches - ActivityHub", layout="wide")
st.title("Your Top Matches")
st.caption(
    "Based on your preferences, we think you'd love these — even if you "
    "hadn't thought of them yourself."
)

user_id = st.session_state.get("user_id")
if not user_id:
    st.warning("No quiz found. Please take the quiz first.")
    if st.button("Go to Quiz"):
        st.switch_page("pages/1_Quiz.py")
    st.stop()

try:
    r = requests.post(f"{API_URL}/recommend/", json={"user_id": user_id}, timeout=15)
    r.raise_for_status()
    data = r.json()
    recs = data.get("recommendations", [])
except requests.RequestException as e:
    st.error(f"Couldn't load recommendations: {e}")
    st.stop()

if not recs:
    st.info("No matches found. Try adjusting your budget or district.")
    st.stop()

# Show activity mix summary at top
activities_in_recs = [r["activity_type"].title() for r in recs]
st.markdown(f"Your mix: {' · '.join(activities_in_recs)}")
st.divider()

for rec in recs:
    with st.container(border=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            emoji = ACTIVITY_EMOJI.get(rec["activity_type"].lower(), "🎯")
            st.markdown(f"### {emoji} {rec['style']}")
            st.markdown(f"{rec['studio_name']} · _{rec['activity_type'].title()}_")
            st.write(
                f"📅 {rec['day']}  🕐 {rec['time']}  💰 {rec['price_amd']:,} AMD"
            )
        with c2:
            pct = int(rec["score"] * 100)
            st.markdown(
                f"<div style='text-align:center; font-size:32px; "
                f"font-weight:bold; color:#2E8B57;'>{pct}%</div>"
                f"<div style='text-align:center; color:gray;'>match</div>",
                unsafe_allow_html=True,
            )

st.divider()
if st.button("← Retake Quiz"):
    st.switch_page("pages/1_Quiz.py")