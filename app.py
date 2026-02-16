import streamlit as st
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import plotly.graph_objs as go
import io

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
    st.header("📓 Upload & View Notebook with Interactive Charts")

    uploaded_file = st.file_uploader(
        "Upload your .ipynb file",
        type=["ipynb"]
    )

    if uploaded_file is not None:
        try:
            # Read notebook
            notebook = nbformat.read(uploaded_file, as_version=4)

            # Execute the notebook (this runs all cells)
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
            ep.preprocess(notebook, {'metadata': {'path': './'}})

            # Loop through all cells
            for cell in notebook['cells']:
                if cell.cell_type == 'code':
                    # Check for Plotly figure objects
                    outputs = cell.get('outputs', [])
                    for output in outputs:
                        if output.output_type == 'execute_result' or output.output_type == 'display_data':
                            data = output.get('data', {})
                            # If it's a plotly figure
                            if 'application/vnd.plotly.v1+json' in data:
                                fig_dict = data['application/vnd.plotly.v1+json']
                                fig = go.Figure(fig_dict)
                                st.plotly_chart(fig, use_container_width=True)
                            # If it's plain text or HTML output
                            elif 'text/plain' in data:
                                st.text(data['text/plain'])
                            elif 'text/html' in data:
                                st.components.v1.html(data['text/html'], height=600, scrolling=True)

        except Exception as e:
            st.error(f"Error executing notebook: {e}")
