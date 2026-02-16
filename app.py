import streamlit as st
import nbformat
from nbconvert import HTMLExporter
from streamlit.components.v1 import html
import os

st.set_page_config(page_title="Project App", layout="wide")

st.title("📊 Booking Analysis Project")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Notebook Viewer"]
)

# -------- Dashboard --------
if page == "Dashboard":
    st.header("📈 Project Overview")

    st.write("""
    This dashboard presents insights from the booking dataset including:
    - Data cleaning and preprocessing
    - Revenue analysis
    - Booking trends
    - Route performance
    - Cancellation patterns
    """)

    st.success("Use the sidebar to view the notebook.")

# -------- Notebook Viewer --------
elif page == "Notebook Viewer":
    st.header("📓 Project Notebook")

    notebook_path = "/mnt/data/Shyamoli_project_Sneha.ipynb"

    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        html_exporter = HTMLExporter()
        body, _ = html_exporter.from_notebook_node(notebook)

        html(body, height=900, scrolling=True)

    except Exception as e:
        st.error(f"Error loading notebook: {e}")
