import streamlit as st
import requests

st.title("CortextECE Interface")

if st.button("Check API Health"):
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            st.success(f"Backend Response: {response.json()}")
        else:
            st.error(f"Backend returned an error: {response.status_code}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")