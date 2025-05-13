import streamlit as st
import joblib
from predict_page import show_predict_page
from explore import show_explore_page
from dashboard_page import show_dashboard_page

# Sidebar Navigation
page = st.sidebar.selectbox("Select Page", ("Predict", "Explore", "Dashboard"))

if page == "Predict":
    show_predict_page()
elif page == "Explore":
    show_explore_page()
else:
    show_dashboard_page()
