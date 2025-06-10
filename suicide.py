import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page config
st.set_page_config(page_title="Suicide Statistics Analysis", layout="wide")

# Load the dataset
@st.cache_data  # This decorator caches the data to avoid reloading on every interaction
def load_data():
    try:
        df = pd.read_csv("who_suicide_statistics.csv")
        df.dropna(inplace=True)
        return df
    except FileNotFoundError:
        st.error("File not found. Please make sure 'who_suicide_statistics.csv' is in the same directory.")
        return None

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filter Data")
    
    # Year selector
    year_range = sorted(df['year'].unique())
    selected_year = st.sidebar.select_slider(
        "Select Year",
        options=year_range,
        value=2010
    )
    
    # Gender selector
    gender_options = df['sex'].unique()
    selected_gender = st.sidebar.radio(
        "Select Gender",
        gender_options,
        index=0
    )
    
    # Age group selector
    age_options = sorted(df['age'].unique())
    selected_age = st.sidebar.selectbox(
        "Select Age Group",
        age_options,
        index=age_options.index("35-54 years") if "35-54 years" in age_options else 0
    )
    
    # Apply filters
    filtered_df = df[
        (df["year"] == selected_year) &
        (df["sex"] == selected_gender) &
        (df["age"] == selected_age)
    ]
    
    # Main content
    st.title("WHO Suicide Statistics Analysis")
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Selected Year", selected_year)
    with col2:
        st.metric("Gender", selected_gender)
    with col3:
        st.metric("Age Group", selected_age)
    
    st.divider()
    
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Total Suicides", filtered_df['suicides_no'].sum())
    with col5:
        st.metric("Countries in Selection", filtered_df['country'].nunique())
    
    # Top 10 countries
    st.subheader(f"Top 10 Countries by Suicide Count ({selected_year})")
    top_countries = filtered_df.groupby("country")["suicides_no"].sum().sort_values(ascending=False).head(10)
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="Blues_r", ax=ax1)
    ax1.set_title(f"Top 10 Countries by Suicides ({selected_year}, {selected_gender}, {selected_age})")
    ax1.set_xlabel("Number of Suicides")
    st.pyplot(fig1)
    
    # Global trend plot
    st.subheader("Global Suicide Trend (1985–2016)")
    trend_df = df.groupby("year")["suicides_no"].sum().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="year", y="suicides_no", data=trend_df, marker="o", ax=ax2)
    ax2.set_title("Global Suicide Trend Over Time")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Total Suicides")
    st.pyplot(fig2)
    
    # Show raw data option
    if st.checkbox("Show filtered raw data"):
        st.dataframe(filtered_df)
    
    # Download button for filtered data
    st.download_button(
        label="Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name=f"suicide_data_{selected_year}_{selected_gender}_{selected_age.replace(' ', '_')}.csv",
        mime='text/csv'
    )
