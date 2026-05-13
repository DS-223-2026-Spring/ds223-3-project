"""
Recommendations page — top 3 class matches plus booking feedback.
"""
import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://api:8000")

ACTIVITY_EMOJI = {"yoga": "🧘", "dance": "💃", "fitness": "💪"}

st.set_page_config(page_title="Your Matches - ActivityHub", layout="wide")
st.title("Your Top Matches")
st.caption(
    "Based on your preferences, we think you'd love these, even if you "
    "hadn't thought of them yourself."
)

user_id = st.session_state.get("user_id")
if not user_id:
    st.info("Take the quiz first to see your matches!")
    st.caption("It only takes 2 minutes.")
    if st.button("Take the Quiz", type="primary", use_container_width=True):
        st.switch_page("pages/1_Quiz.py")
    st.stop()

try:
    with st.spinner("Finding your matches..."):
        r = requests.post(f"{API_URL}/recommend/", json={"user_id": user_id}, timeout=10)
        r.raise_for_status()
        data = r.json()
        recs = data.get("recommendations", [])
except requests.RequestException as e:
    st.error(f"Couldn't load recommendations: {e}")
    st.stop()

if not recs:
    st.info("No matches found. Try adjusting your budget or district.")
    st.stop()

if len(recs) < 3:
    st.info(f"We found {len(recs)} strong match{'es' if len(recs) > 1 else ''} for you. Try widening your budget or district to see more.")

# Activity mix summary
activities_in_recs = [rec["activity_type"].title() for rec in recs]
st.markdown(f"**Your mix:** {' · '.join(activities_in_recs)}")
st.divider()

# Render each recommendation
for rec in recs:
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            emoji = ACTIVITY_EMOJI.get(rec["activity_type"].lower(), "🎯")
            st.markdown(f"### {emoji} {rec['style']}")
            st.markdown(f"**{rec['studio_name']}** · _{rec['activity_type'].title()}_")
            st.write(
                f"📅 {rec['day']}  |  🕐 {rec['time']}  |  💰 {rec['price_amd']:,} AMD"
            )
        with c2:
            pct = int(rec["score"] * 100)
            delta = f"+{pct - 50}" if pct > 50 else None
            st.metric(label="Match", value=f"{pct}%", delta=delta)
        with c3:
            if st.button("I tried this", key=f"book_{rec['class_id']}"):
                try:
                    payload = {
                        "user_id": user_id,
                        "class_id": rec["class_id"],
                        "feedback": "tried",
                    }
                    requests.post(
                        f"{API_URL}/bookings/", json=payload, timeout=10
                    ).raise_for_status()
                    st.success("Thanks! Your feedback helps us improve.")
                    st.balloons()
                except requests.RequestException as e:
                    st.error(f"Couldn't save: {e}")

st.divider()

# Show user's booking history
try:
    bookings_r = requests.get(f"{API_URL}/bookings/{user_id}", timeout=10)
    bookings_r.raise_for_status()
    bookings = bookings_r.json()
except requests.RequestException:
    bookings = []

if bookings:
    st.divider()
    st.subheader("Classes you've tried")
    st.caption("Your feedback helps us learn what matches your preferences.")
    for b in bookings[:5]:  # show last 5
        st.write(f"• **{b['style']}** at {b['studio_name']} ({b['activity_type']})")
        
c1, c2 = st.columns(2)
with c1:
    if st.button("Retake Quiz"):
        st.switch_page("pages/1_Quiz.py")
with c2:
    if st.button("View Studio Insights"):
        st.switch_page("pages/3_Studio_Dashboard.py")