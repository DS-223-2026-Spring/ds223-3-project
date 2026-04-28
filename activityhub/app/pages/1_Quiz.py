
import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://api:8000")

DISTRICTS = [
    "Kentron", "Arabkir", "Davtashen", "Ajapnyak", "Nor Nork",
    "Shengavit", "Erebuni", "Malatia-Sebastia", "Avan", "Kanaker-Zeytun",
]

st.set_page_config(page_title="Quiz - ActivityHub", layout="centered")
st.title("Onboarding Quiz")
st.caption(
    "Tell us about yourself. We'll find activities that match who you are,"
    "you don't need to know what you want yet."
)

with st.form("quiz"):
    st.subheader("About you")
    age = st.number_input("Age", 15, 80, 22)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    district = st.selectbox("Your district in Yerevan", DISTRICTS)

    st.subheader("Your personality & experience")
    experience = st.selectbox(
        "Your overall experience level with physical activities",
        ["Beginner", "Intermediate", "Advanced"],
    )
    group = st.radio(
        "Do you prefer group or private sessions?",
        ["Group", "Private", "No preference"],
        horizontal=True,
    )
    energy = st.radio(
        "What kind of environment fits you?",
        ["Calm", "High", "Depends on mood"],
        horizontal=True,
    )
    structure = st.radio(
        "How do you like to learn or practice?",
        ["Structured", "Freestyle", "Mix"],
        horizontal=True,
        help="Structured = instructor-led. Freestyle = your own flow.",
    )
    goal = st.selectbox(
        "What's your primary goal?",
        [
            "Physical fitness / health",
            "Stress relief",
            "Creative expression",
            "Learning a new skill",
            "Social",
        ],
    )

    st.subheader("Practical stuff")
    budget = st.number_input(
        "Max budget per session (AMD)", 1000, 20000, 5000, step=500,
    )
    travel = st.selectbox(
        "Max travel distance",
        ["Under 1km", "Under 5km", "Under 10km", "Over 10km"],
        index=1,
    )
    days = st.multiselect(
        "Preferred days (optional)",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    )
    preferred_time = st.selectbox(
        "Preferred time",
        ["morning", "afternoon", "evening", "any"],
        index=3,
    )

    submitted = st.form_submit_button("Get My Recommendations", type="primary")

if submitted:
    payload = {
        "age": int(age),
        "gender": gender,
        "district": district,
        "experience_level": experience,
        "group_preference": group,
        "energy_preference": energy,
        "structure_preference": structure,
        "goal": goal,
        "budget_max_amd": int(budget),
        "preferred_days": days,
        "preferred_time": preferred_time,
        "max_travel_km": travel,
    }

    try:
        with st.spinner("Finding your matches..."):
            r = requests.post(f"{API_URL}/quiz/", json=payload, timeout=10)
            r.raise_for_status()
            data = r.json()
            st.session_state["user_id"] = data["user_id"]
        st.success("Got it! Redirecting to your recommendations...")
        st.switch_page("pages/2_Recommendations.py")
    except requests.RequestException as e:
        st.error(f"Couldn't reach the API: {e}")