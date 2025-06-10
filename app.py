import streamlit as st
import pandas as pd
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    st.error(f"Critical package missing: {e}. Check requirements.txt!")
    st.stop()

# Configure page
st.set_page_config(layout="wide")

# Load data from URL (more reliable in cloud)
@st.cache_data
def load_data():
    try:
        url = "https://raw.githubusercontent.com/who/gho-data/main/suicide-statistics.csv"  # Example URL
        return pd.read_csv(url).dropna()
    except Exception as e:
        st.error(f"Data load failed: {e}")
        return None

df = load_data()

if df is not None:
    st.title("WHO Suicide Data Analysis")
    
    # Filters
    col1, col2 = st.columns(2)
    year = col1.selectbox("Year", sorted(df['year'].unique()))
    age = col2.selectbox("Age Group", sorted(df['age'].unique()))
    
    # Filter data
    filtered = df[(df.year == year) & (df.age == age)]
    
    # Visualizations
    fig, ax = plt.subplots()
    sns.barplot(
        data=filtered.nlargest(10, 'suicides_no'),
        x='suicides_no',
        y='country',
        palette='viridis',
        ax=ax
    )
    st.pyplot(fig)
