import streamlit as st
import nbformat
from nbconvert import HTMLExporter
from streamlit.components.v1 import html

st.title("📓 Notebook Viewer")

# Path to your notebook file
notebook_path = "Shyamoli_project_Sneha.ipynb"

try:
    # Load notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Convert to HTML
    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(notebook)

    # Display in Streamlit
    html(body, height=800, scrolling=True)

except FileNotFoundError:
    st.error("Notebook file not found. Make sure it is in the project folder.")
