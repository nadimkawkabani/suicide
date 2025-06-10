import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page
st.set_page_config(page_title="Suicide Data Analysis", layout="wide")

# Load data with error handling
@st.cache_data
def load_data():
    try:
        # Try online first (replace with your actual URL)
        url = "https://raw.githubusercontent.com/your-username/your-repo/main/who_suicide_statistics.csv"
        df = pd.read_csv(url)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

df = load_data()

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    year = st.sidebar.selectbox("Year", sorted(df['year'].unique()))
    gender = st.sidebar.radio("Gender", df['sex'].unique())
    age = st.sidebar.selectbox("Age Group", sorted(df['age'].unique()))

    # Filter data
    filtered = df[(df['year'] == year) & (df['sex'] == gender) & (df['age'] == age)]

    # Metrics
    st.title("Suicide Statistics Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Total Cases", filtered['suicides_no'].sum())
    col2.metric("Countries", filtered['country'].nunique())

    # Plot top countries
    st.subheader(f"Top Countries in {year}")
    top = filtered.groupby('country')['suicides_no'].sum().nlargest(10)
    
    fig, ax = plt.subplots()
    sns.barplot(x=top.values, y=top.index, palette="rocket")
    st.pyplot(fig)

    # Global trend plot
    st.subheader("Historical Trend")
    trend = df.groupby('year')['suicides_no'].sum().reset_index()
    
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=trend, x='year', y='suicides_no')
    st.pyplot(fig2)
