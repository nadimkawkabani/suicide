import streamlit as st
import pandas as pd
import sys

# Package installation check
def check_packages():
    required = {
        'matplotlib': '3.7.1',
        'seaborn': '0.12.2',
        'pandas': '1.5.3'
    }
    
    missing = []
    for pkg, ver in required.items():
        try:
            mod = __import__(pkg)
            if mod.__version__ != ver:
                missing.append(f"{pkg}=={ver} (found {mod.__version__})")
        except ImportError:
            missing.append(f"{pkg}=={ver} (missing)")
    
    if missing:
        st.error(f"CRITICAL: Missing/incorrect packages:\n- " + "\n- ".join(missing))
        st.error("""
        Your requirements.txt MUST contain exactly:
        matplotlib==3.7.1
        seaborn==0.12.2
        pandas==1.5.3
        """)
        st.stop()

check_packages()

# Now safely import visualization packages
import matplotlib
matplotlib.use('Agg')  # Essential for Streamlit Cloud
import matplotlib.pyplot as plt
import seaborn as sns

# Demo visualization
st.title("Package Verification Successful!")
st.balloons()

# Create sample plot
fig, ax = plt.subplots()
sns.barplot(
    x=['A', 'B', 'C'],
    y=[10, 20, 15],
    palette='viridis',
    ax=ax
)
ax.set_title("Seaborn Plot Working!")
st.pyplot(fig)

# Show environment info
st.subheader("Environment Information")
st.code(f"""
Python: {sys.version}
Matplotlib: {matplotlib.__version__}
Seaborn: {sns.__version__}
Pandas: {pd.__version__}
""")
