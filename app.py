import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Booking Analysis Dashboard", layout="wide")

st.title("🚌 Booking Data Analysis Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your dataset CSV", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # -------- Data Cleaning --------
    df = df.copy()

    if "Email" in df.columns:
        df["Email"] = df["Email"].fillna("Not Provided")

    if "Issued On" in df.columns:
        df["Issued On"] = pd.to_datetime(df["Issued On"], dayfirst=True, errors="coerce")

    if "Booked On" in df.columns:
        df["Booked On"] = pd.to_datetime(df["Booked On"], dayfirst=True, errors="coerce")

    if "Journey Date" in df.columns:
        df["Journey Date"] = pd.to_datetime(df["Journey Date"], dayfirst=True, errors="coerce")

    # -------- KPIs --------
    st.header("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    total_bookings = len(df)
    total_revenue = df["Net Amount"].sum() if "Net Amount" in df.columns else 0
    total_routes = df["Route"].nunique() if "Route" in df.columns else 0

    col1.metric("Total Bookings", total_bookings)
    col2.metric("Total Revenue", f"{total_revenue:,.2f}")
    col3.metric("Unique Routes", total_routes)

    # -------- Channel Analysis --------
    if "Booked By" in df.columns:
        st.subheader("📌 Booking Channel Distribution")
        channel_counts = df["Booked By"].value_counts()
        st.bar_chart(channel_counts)

    # -------- Status Analysis --------
    if "Status" in df.columns:
        st.subheader("📌 Booking Status")
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)

    # -------- Top Boarding Points --------
    if "Boarding Point" in df.columns:
        st.subheader("📌 Top Boarding Points")
        top_boarding = df["Boarding Point"].value_counts().head(5)
        st.bar_chart(top_boarding)

    # -------- Revenue by Route --------
    if "Route" in df.columns and "Net Amount" in df.columns:
        st.subheader("💰 Revenue by Route")
        route_rev = df.groupby("Route")["Net Amount"].sum().sort_values(ascending=False)
        st.bar_chart(route_rev.head(10))

    # -------- Cancellation Rate --------
    if "Status" in df.columns:
        cancel_rate = (df["Status"].str.lower() == "cancel").mean() * 100
        st.subheader("⚠️ Cancellation Rate")
        st.write(f"{cancel_rate:.2f}%")

else:
    st.info("Please upload your CSV file to begin.")
