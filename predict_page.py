import streamlit as st
import joblib
import pandas as pd
import numpy as np
import time

# Load the saved model and preprocessor
model = joblib.load('best_salary_model.pkl')
preprocessor = joblib.load('salary_preprocessor.pkl')

# Map numerical salary to a readable range
def map_salary_to_range(salary):
    if salary < 10000:
        return "<10,000"
    elif 10000 <= salary < 20000:
        return "$10,000 - 19,999"
    elif 20000 <= salary < 40000:
        return "$20,000 - 39,999"
    elif 40000 <= salary < 60000:
        return "$40,000 - 59,999"
    elif 60000 <= salary < 80000:
        return "$60,000 - 79,999"
    elif 80000 <= salary < 100000:
        return "$80,000 - 99,999"
    else:
        return ">100,000"

def show_predict_page():
    # Sidebar
    with st.sidebar:
        st.title("🧠 About This Project")
        st.write("This app predicts software developer salaries based on your profile.")
        st.markdown("---")
        st.write("Built with  using XGBoost, Scikit-learn, and Streamlit.")
    
    # Main Title
    st.title("💻 Software Developer Salary Prediction 💰")
    st.write("## Fill in your details to estimate your potential salary 🚀")

    # --- Options for Dropdowns ---
    country_options = [
        "United States", "India", "United Kingdom", "Germany", "Canada", "Brazil",
        "France", "Spain", "Australia", "Netherlands", "Poland", "Italy", 
        "Russian Federation", "Sweden"
    ]

    education_levels = [
        "Less than a Bachelors", "Bachelor’s degree", "Master’s degree", "Post grad"
    ]

    gender_options = ["Man", "Woman", "Other"]

    major_options = [
        "Computer Science", "Information Technology", "Engineering", "Mathematics",
        "Physics", "Other"
    ]

    devtype_options = [
        "Developer, full-stack", "Developer, back-end", "Developer, front-end", 
        "Developer, mobile", "Engineer, data", "Developer, game", "Developer, embedded", "Other"
    ]

    language_options = [
        "Python", "JavaScript", "Java", "C#", "C++", "TypeScript", "SQL", "PHP", "Other"
    ]

    database_options = [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "Microsoft SQL Server", "Other"
    ]

    # --- UI Inputs ---
    country = st.selectbox("🌎 Country", country_options)
    education = st.selectbox("🎓 Education Level", education_levels)
    gender = st.selectbox("🚻 Gender", gender_options)
    major = st.selectbox("📚 Undergraduate Major", major_options)
    dev_type = st.selectbox("👨‍💻 Developer Type", devtype_options)

    language_worked_with = st.multiselect("🧑‍💻 Languages Worked With", language_options)
    database_worked_with = st.multiselect("🛢️ Databases Worked With", database_options)

    experience = st.slider("⌛ Years of Professional Experience", 0, 50, 3)

    ok = st.button("🚀 Calculate Salary")

    if ok:
        with st.spinner('🔄 Preparing your data...'):
            try:
                # Progress Bar
                progress = st.progress(0)
                for perc_completed in range(100):
                    progress.progress(perc_completed + 1)
                    time.sleep(0.01)

                # Prepare inputs
                input_dict = {
                    'Country': country,
                    'EdLevel': education,
                    'YearsCodePro': experience,
                    'Gender': gender,
                    'UndergradMajor': major,
                    'DevType': dev_type,
                    'LanguageWorkedWith': ",".join(language_worked_with),
                    'DatabaseWorkedWith': ",".join(database_worked_with),
                }

                input_df = pd.DataFrame([input_dict])

                # Preprocess
                X_processed = preprocessor.transform(input_df)

                # Predict
                predicted_salary = model.predict(X_processed)[0]
                predicted_salary_range = map_salary_to_range(predicted_salary)

                # Show output
                st.success(f"🎯 The estimated salary range is: **{predicted_salary_range}**")
                st.balloons()

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
