import streamlit as st
import sys
from importlib.metadata import version

# Package verification
st.title("Package Installation Checker")

try:
    import matplotlib
    import seaborn
    import pandas
    
    st.success("✅ All packages imported successfully!")
    
    # Display versions
    st.subheader("Installed Versions")
    st.code(f"""
    Python: {sys.version}
    Matplotlib: {version('matplotlib')}
    Seaborn: {version('seaborn')}
    Pandas: {version('pandas')}
    Streamlit: {version('streamlit')}
    """)
    
    # Simple plot test
    st.subheader("Plot Test")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([1,2,3], [1,2,3])
    st.pyplot(fig)
    
except ImportError as e:
    st.error(f"❌ Import failed: {e}")
    st.error("""
    Critical packages missing! Verify your requirements.txt contains:
    matplotlib-base==3.7.1
    seaborn==0.12.2
    pandas==1.5.3
    """)
