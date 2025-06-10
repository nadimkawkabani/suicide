import streamlit as st
import pandas as pd

# First try to import visualization packages
try:
    import matplotlib
    matplotlib.use('Agg')  # Critical for Streamlit Cloud
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    st.error("""
    Packages not installed! Verify your requirements.txt contains:
    matplotlib==3.7.1
    seaborn==0.12.2
    """)
    st.stop()

# Load sample data if real data fails
@st.cache_data
def load_data():
    try:
        # Try from URL first
        url = "https://raw.githubusercontent.com/plotly/datasets/master/school_earnings.csv"
        return pd.read_csv(url)
    except:
        # Fallback to demo data
        return pd.DataFrame({
            'Country': ['USA', 'China', 'Japan'],
            'Suicides': [50000, 30000, 20000]
        })

df = load_data()

# Simple visualization
st.title("Suicide Data Demo")
fig, ax = plt.subplots()
sns.barplot(data=df, x='Country', y='Suicides', ax=ax)
st.pyplot(fig)
