import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Page Config ----------------
st.set_page_config(page_title="Booking Analysis Dashboard", layout="wide")

st.title("📊 Booking Analysis Dashboard")

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader("Upload your booking CSV file", type=["csv"])

if uploaded_file is not None:

    # Load data
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # ---------------- Data Preview ----------------
    with st.expander("Preview Dataset"):
        st.dataframe(df.head())

    # ---------------- KPI Section ----------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(df))

    if "revenue" in df.columns:
        total_revenue = df["revenue"].sum()
        col2.metric("Total Revenue", f"${total_revenue:,.2f}")

    if "canceled" in df.columns:
        cancel_rate = df["canceled"].mean() * 100
        col3.metric("Cancellation Rate", f"{cancel_rate:.2f}%")

    # ---------------- Booking Trend ----------------
    if "booking_date" in df.columns:
        st.subheader("📈 Booking Trend")

        df["booking_date"] = pd.to_datetime(df["booking_date"], errors="coerce")
        trend = df.groupby(df["booking_date"].dt.to_period("M")).size()
        trend.index = trend.index.astype(str)

        fig1, ax1 = plt.subplots()
        trend.plot(kind="line", marker="o", ax=ax1)
        plt.xticks(rotation=45)
        plt.title("Monthly Booking Trend")
        st.pyplot(fig1)

    # ---------------- Revenue by Category / Route ----------------
    if "route" in df.columns and "revenue" in df.columns:
        st.subheader("💰 Revenue by Route")

        route_rev = df.groupby("route")["revenue"].sum().sort_values(ascending=False).head(10)

        fig2, ax2 = plt.subplots()
        route_rev.plot(kind="bar", ax=ax2)
        plt.xticks(rotation=45)
        plt.title("Top 10 Routes by Revenue")
        st.pyplot(fig2)

    # ---------------- Cancellation Distribution ----------------
    if "canceled" in df.columns:
        st.subheader("❌ Cancellation Distribution")

        fig3, ax3 = plt.subplots()
        sns.countplot(x="canceled", data=df, ax=ax3)
        plt.title("Cancellation Count")
        st.pyplot(fig3)

else:
    st.info("Please upload a CSV file to view the dashboard.")
