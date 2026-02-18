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

    # -------- DOWNLOAD REPORT BUTTON --------
    st.subheader("⬇️ Download Project Report")

    try:
        with open("Shyamoli Project (Report)_Sneha Nath.docx", "rb") as file:
            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name="Booking_Analysis_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except:
        st.warning("Report file not found. Put the file in the same folder as this app.")

# ---------------- Notebook Viewer ----------------
elif page == "Notebook Viewer":
    st.header("📓 Upload & View Notebook")

    uploaded_file = st.file_uploader(
        "Upload your .ipynb file",
        type=["ipynb"]
    )

    if uploaded_file is not None:
        try:
            # -------- NOTEBOOK DOWNLOAD BUTTON --------
            st.download_button(
                label="📥 Download Notebook",
                data=uploaded_file,
                file_name=uploaded_file.name,
                mime="application/octet-stream"
            )

            # Read notebook
            notebook = nbformat.read(uploaded_file, as_version=4)

            # Export notebook as HTML
            html_exporter = HTMLExporter()
            html_exporter.template_name = 'classic'

            body, resources = html_exporter.from_notebook_node(notebook)

            # Embed images in base64
            for name, data in resources.get('outputs', {}).items():
                if 'image/png' in data:
                    img_b64 = data['image/png']
                    body = body.replace(
                        f'attachment:{name}',
                        f'data:image/png;base64,{img_b64}'
                    )

            # Display HTML
            html(body, height=900, scrolling=True)

        except Exception as e:
            st.error(f"Error loading notebook: {e}")
