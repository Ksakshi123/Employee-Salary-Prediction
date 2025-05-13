import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df[df["Employment"] == "Employed full-time"]
    df = df.dropna()
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_dashboard_page():
    st.title("📊 Developer Salary Dashboard")

    st.write("### Insights based on Stack Overflow Developer Survey")

    # --- Filters ---
    countries = df["Country"].unique()
    country_filter = st.selectbox("🌎 Select a Country to Filter", options=["All"] + list(countries))

    if country_filter != "All":
        df_filtered = df[df["Country"] == country_filter]
    else:
        df_filtered = df.copy()

    # --- Top Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Average Salary", f"${int(df_filtered['Salary'].mean()):,}")
    col2.metric("🌍 Countries", df_filtered['Country'].nunique())
    col3.metric("🧑‍💻 Data Points", len(df_filtered))

    st.write("---")

    # --- Country Distribution ---
    st.subheader("🌍 Top Countries by Number of Developers")
    country_counts = df_filtered["Country"].value_counts().head(10)
    fig_country = px.bar(country_counts, x=country_counts.index, y=country_counts.values, labels={'y':'Count', 'x':'Country'}, title="Top Countries")
    st.plotly_chart(fig_country)

    st.write("---")

    # --- Salary vs Education ---
    st.subheader("🎓 Average Salary by Education Level")
    education_salary = df_filtered.groupby("EdLevel")["Salary"].mean().sort_values(ascending=True)
    fig_education = px.bar(education_salary, x=education_salary.index, y=education_salary.values, labels={'y':'Average Salary', 'x':'Education Level'}, title="Salary by Education")
    st.plotly_chart(fig_education)

    st.write("---")

    # --- Salary vs Experience ---
    st.subheader("⌛ Salary based on Years of Professional Experience")
    df_filtered["YearsCodePro"] = df_filtered["YearsCodePro"].replace({"Less than 1 year": 0.5, "More than 50 years": 50})
    df_filtered["YearsCodePro"] = df_filtered["YearsCodePro"].astype(float)
    experience_salary = df_filtered.groupby("YearsCodePro")["Salary"].mean()
    fig_experience = px.line(x=experience_salary.index, y=experience_salary.values, labels={'x':'Years of Experience', 'y':'Average Salary'}, title="Experience vs Salary")
    st.plotly_chart(fig_experience)

    st.success("✅ Dashboard Loaded Successfully!")
