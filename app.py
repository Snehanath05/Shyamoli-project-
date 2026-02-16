import streamlit as st
import nbformat
from nbconvert import HTMLExporter
from streamlit.components.v1 import html
import base64

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
            # Read notebook
            notebook = nbformat.read(uploaded_file, as_version=4)

            # Export notebook as HTML (with embedded images and charts)
            html_exporter = HTMLExporter()
            html_exporter.template_name = 'classic'  # 'classic' template preserves outputs

            body, resources = html_exporter.from_notebook_node(notebook)

            # Save images in base64 so charts are visible
            for name, data in resources.get('outputs', {}).items():
                if 'image/png' in data:
                    img_b64 = data['image/png']
                    body = body.replace(f'attachment:{name}', f'data:image/png;base64,{img_b64}')

            # Display HTML in Streamlit
            html(body, height=900, scrolling=True)

        except Exception as e:
            st.error(f"Error loading notebook: {e}")
