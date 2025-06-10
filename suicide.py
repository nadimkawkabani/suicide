import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Suicide Statistics Analysis", layout="wide")

# Load data (with caching)
@st.cache_data
def load_data():
    try:
        # Try local file first
        df = pd.read_csv("who_suicide_statistics.csv")
        df.dropna(inplace=True)
        return df
    except FileNotFoundError:
        # Fallback to online file (replace with your actual URL)
        try:
            df = pd.read_csv("https://raw.githubusercontent.com/yourusername/yourrepo/main/who_suicide_statistics.csv")
            df.dropna(inplace=True)
            return df
        except Exception as e:
            st.error(f"Failed to load data: {e}")
            return None

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filter Data")
    
    # Year selector
    selected_year = st.sidebar.selectbox(
        "Select Year",
        sorted(df['year'].unique()),
        index=len(df['year'].unique()) - 6  # Default to ~2010
    )
    
    # Gender selector
    selected_gender = st.sidebar.radio(
        "Select Gender",
        df['sex'].unique(),
        index=0
    )
    
    # Age group selector
    selected_age = st.sidebar.selectbox(
        "Select Age Group",
        sorted(df['age'].unique()),
        index=3 if "35-54 years" in df['age'].unique() else 0
    )
    
    # Apply filters
    filtered_df = df[
        (df["year"] == selected_year) &
        (df["sex"] == selected_gender) &
        (df["age"] == selected_age)
    ]
    
    # Main content
    st.title("WHO Suicide Statistics Analysis")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Suicides", f"{filtered_df['suicides_no'].sum():,}")
    col2.metric("Countries", filtered_df['country'].nunique())
    col3.metric("Year Analyzed", selected_year)
    
    # Top 10 countries chart
    st.subheader(f"Top 10 Countries by Suicide Count")
    top_countries = filtered_df.groupby("country")["suicides_no"].sum().nlargest(10)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="viridis", ax=ax)
    ax.set_xlabel("Number of Suicides")
    st.pyplot(fig)
    
    # Global trend
    st.subheader("Global Suicide Trend Over Time")
    trend_df = df.groupby("year")["suicides_no"].sum().reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=trend_df, x="year", y="suicides_no", marker="o", ax=ax2)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Total Suicides")
    st.pyplot(fig2)
    
    # Data download
    st.download_button(
        "Download Filtered Data",
        filtered_df.to_csv(index=False),
        f"suicide_data_{selected_year}_{selected_gender}_{selected_age.replace(' ', '_')}.csv"
    )
