import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('/Users/nadimkawkabani/Desktop/Healthcare Analytics/who_suicide_statistics.csv')

# Title and intro
st.title("Suicide Rates Overview")
st.markdown("Analyzing suicide rates from 1985 to 2016 based on WHO data.")

# Sidebar filters
year = st.sidebar.selectbox("Select Year", sorted(df['year'].unique()))
gender = st.sidebar.selectbox("Select Gender", df['sex'].unique())
age = st.sidebar.selectbox("Select Age Group", df['age'].unique())

# Filtered data
filtered_df = df[(df['year'] == year) & (df['sex'] == gender) & (df['age'] == age)]

# Chart: Suicide by country
country_data = filtered_df.groupby('country')['suicides_no'].sum().sort_values(ascending=False).head(10)
fig = px.bar(country_data, x=country_data.index, y=country_data.values, labels={'x': 'Country', 'y': 'Suicides'})
st.plotly_chart(fig)

# Show table
st.subheader("Filtered Data")
st.dataframe(filtered_df)
