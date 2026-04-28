import streamlit as st

st.set_page_config(page_title="ActivityHub", layout="wide")

st.title("ActivityHub")
st.subheader("Find the perfect class for you in Yerevan")
st.markdown(
    "Take a 2-minute quiz and get personalized recommendations for dance, "
    "yoga, fitness, and music classes that match your personality, schedule, and goals."
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Take the Quiz →", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Quiz.py")