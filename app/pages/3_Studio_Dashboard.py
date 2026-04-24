
import os
import streamlit as st
import requests
import pandas as pd

API_URL = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="Studio Dashboard - ActivityHub", layout="wide")
st.title("Studio Audience Insights")
st.caption("Which user segments are most likely to book your classes")

try:
    r = requests.get(f"{API_URL}/segments/", timeout=10)
    r.raise_for_status()
    segments = r.json()
except requests.RequestException as e:
    st.error(f"Couldn't load segments: {e}")
    st.stop()

if not segments:
    st.info("No segments available yet.")
    st.stop()

total_users = sum(s.get("size", 0) for s in segments)
avg_booking = sum(s.get("booking_likelihood", 0) * s.get("size", 0)
                  for s in segments) / max(total_users, 1)

k1, k2, k3 = st.columns(3)
k1.metric("Matched Users", total_users)
k2.metric("Predicted Booking Rate", f"{avg_booking * 100:.0f}%")
k3.metric("Segments", len(segments))

df = pd.DataFrame(segments)
df["booking_likelihood"] = df["booking_likelihood"].apply(lambda x: f"{x * 100:.0f}%")
st.dataframe(df, use_container_width=True, hide_index=True)