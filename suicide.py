import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Suicide Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("suicide_rates.csv")
    df = df.dropna()
    df = df[df['suicides_no'] >= 0]  # filter out any invalid entries
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filters")
selected_year = st.sidebar.selectbox("Year", sorted(df["year"].unique()))
selected_gender = st.sidebar.selectbox("Gender", df["sex"].unique())
selected_age = st.sidebar.selectbox("Age Group", df["age"].unique())

# Apply filters
filtered_df = df[
    (df["year"] == selected_year) &
    (df["sex"] == selected_gender) &
    (df["age"] == selected_age)
]

# Title
st.title("📊 Suicide Rates Dashboard (WHO Dataset)")
st.markdown("""
This dashboard allows exploration of global suicide rates from 1985 to 2016. 
Use the filters to segment data by year, gender, and age group.
""")

# Total suicides summary
st.subheader("📌 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Filtered Year", selected_year)
col2.metric("Total Suicides (Filtered)", int(filtered_df["suicides_no"].sum()))
col3.metric("Number of Countries", filtered_df["country"].nunique())

# Chart: Top 10 countries by suicide count
st.subheader(f"🌍 Top 10 Countries with Highest Suicides in {selected_year}")
top_countries = filtered_df.groupby("country")["suicides_no"].sum().sort_values(ascending=False).head(10)
fig1 = px.bar(
    top_countries,
    x=top_countries.index,
    y=top_countries.values,
    labels={"x": "Country", "y": "Number of Suicides"},
    title="Top 10 Countries by Suicide Count",
)
st.plotly_chart(fig1, use_container_width=True)

# Chart: Suicide trend over time (overall, not filtered)
st.subheader("📈 Overall Global Suicide Trend (1985–2016)")
trend_df = df.groupby("year")["suicides_no"].sum().reset_index()
fig2 = px.line(trend_df, x="year", y="suicides_no", title="Suicides Over Time (Global)", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Optional: Show raw data
with st.expander("🗃 View Filtered Data Table"):
    st.dataframe(filtered_df)

# Footer
st.markdown("""
---
📌 *Data Source: [Kaggle - WHO Suicide Statistics](https://www.kaggle.com/datasets/szamil/who-suicide-statistics)*  
Created for **MSBA350 – Healthcare Analytics Project**
""")
