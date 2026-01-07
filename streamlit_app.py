"""
UNLIMITED IRON CREATOR - Streamlit Application

A simple, functional Streamlit application demonstrating basic interactive features.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="UNLIMITED IRON CREATOR",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and welcome message
st.title("⚡ UNLIMITED IRON CREATOR")
st.markdown("---")

# Welcome section
st.header("Welcome!")
st.write("""
Welcome to the UNLIMITED IRON CREATOR application! This is a functional Streamlit app
that demonstrates various interactive features and data visualization capabilities.
""")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.write("Configure your experience:")
    
    user_name = st.text_input("Enter your name:", value="User")
    favorite_color = st.selectbox(
        "Choose your favorite color:",
        ["Red", "Blue", "Green", "Yellow", "Purple"]
    )
    intensity = st.slider("Select intensity level:", 0, 100, 50)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Interactive Demo")
    st.write(f"Hello, **{user_name}**! 👋")
    st.write(f"Your favorite color is: **{favorite_color}**")
    st.write(f"Intensity level: **{intensity}%**")
    
    if st.button("Generate Random Data"):
        st.session_state.show_data = True
    
    if "show_data" in st.session_state and st.session_state.show_data:
        st.success("Data generated successfully!")

with col2:
    st.subheader("Sample Data Visualization")
    
    # Generate sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Series A', 'Series B', 'Series C']
    )
    
    st.line_chart(chart_data)

# Additional features section
st.markdown("---")
st.header("Features")

tab1, tab2, tab3 = st.tabs(["📊 Data", "📈 Charts", "ℹ️ Info"])

with tab1:
    st.subheader("Sample Data Table")
    df = pd.DataFrame({
        'Name': ['Iron', 'Steel', 'Titanium', 'Aluminum'],
        'Strength': [100, 150, 180, 70],
        'Weight': [80, 120, 50, 30],
        'Cost': [10, 20, 50, 15]
    })
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Bar Chart")
    st.bar_chart(df.set_index('Name')['Strength'])

with tab3:
    st.subheader("About This App")
    st.info("""
    This application is built with Streamlit and demonstrates:
    - Interactive widgets (text input, sliders, buttons)
    - Data visualization (line charts, bar charts)
    - Layout components (columns, tabs, sidebar)
    - Session state management
    """)
    
    st.write(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Footer
st.markdown("---")
st.caption("UNLIMITED IRON CREATOR © 2024 | Powered by Streamlit")
