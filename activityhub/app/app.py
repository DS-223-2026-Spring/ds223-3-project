import streamlit as st

st.set_page_config(page_title="ActivityHub", layout="wide")

st.title("ActivityHub")
st.subheader("Find the perfect class for you in Yerevan")
st.markdown(
    "Take a 2-minute quiz and get personalized recommendations for dance, "
    "yoga, and fitness classes that match your personality, schedule, and goals."
)

st.divider()

st.markdown("### How it works")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**1. Tell us about you**")
    st.caption("Age, energy level, goals, budget")
with c2:
    st.markdown("**2. Get your top matches**")
    st.caption("Our model finds 3 classes you'll love across yoga, dance, and fitness.")
with c3:
    st.markdown("**3. Try them**")
    st.caption("Click 'I tried this' so we learn and improve over time.")

st.divider()

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Take the Quiz", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Quiz.py")