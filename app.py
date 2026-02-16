import streamlit as st
import nbformat
from nbconvert import HTMLExporter
from streamlit.components.v1 import html

st.set_page_config(page_title="Booking Analysis Project", layout="wide")

st.title("📊 Booking Analysis Project")

# Sidebar Navigation
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Notebook Viewer"]
)

# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.header("📈 Project Overview")

    st.write("""
    This dashboard presents insights from the booking dataset including:

    - Data Cleaning & Preprocessing  
    - Revenue Analysis  
    - Booking Trends  
    - Route Performance  
    - Cancellation Patterns  
    """)

    st.success("Use the sidebar to view the notebook.")

# ---------------- Notebook Viewer ----------------
elif page == "Notebook Viewer":
    st.header("📓 Upload & View Notebook")

    uploaded_file = st.file_uploader(
        "Upload your .ipynb file",
        type=["ipynb"]
    )

    if uploaded_file is not None:
        try:
            notebook = nbformat.read(uploaded_file, as_version=4)

            html_exporter = HTMLExporter()
            body, _ = html_exporter.from_notebook_node(notebook)

            html(body, height=900, scrolling=True)

        except Exception as e:
            st.error(f"Error loading notebook: {e}")
