import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Booking Analysis Project", layout="wide")

st.title("📊 Booking Analysis Dashboard")

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    # Replace with your actual file
    df = pd.read_csv("your_booking_file.csv")
    return df

df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.header("Filters")

# Example filters
if "booking_date" in df.columns:
    df["booking_date"] = pd.to_datetime(df["booking_date"])
    min_date = df["booking_date"].min()
    max_date = df["booking_date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    df = df[
        (df["booking_date"] >= pd.to_datetime(date_range[0])) &
        (df["booking_date"] <= pd.to_datetime(date_range[1]))
    ]

# ---------------- KPI Section ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Bookings", len(df))

if "revenue" in df.columns:
    col2.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")

if "canceled" in df.columns:
    cancel_rate = df["canceled"].mean() * 100
    col3.metric("Cancellation Rate", f"{cancel_rate:.2f}%")

# ---------------- Charts ----------------
st.subheader("📈 Booking Trends")

if "booking_date" in df.columns:
    trend = df.groupby(df["booking_date"].dt.to_period("M")).size()
    trend.index = trend.index.astype(str)

    fig, ax = plt.subplots()
    trend.plot(kind="line", marker="o", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Monthly Booking Trend")
    st.pyplot(fig)

st.subheader("💰 Revenue by Route")

if "route" in df.columns and "revenue" in df.columns:
    route_rev = df.groupby("route")["revenue"].sum().sort_values(ascending=False)

    fig2, ax2 = plt.subplots()
    route_rev.head(10).plot(kind="bar", ax=ax2)
    plt.xticks(rotation=45)
    plt.title("Top 10 Routes by Revenue")
    st.pyplot(fig2)

st.subheader("❌ Cancellation Analysis")

if "canceled" in df.columns:
    fig3, ax3 = plt.subplots()
    sns.countplot(x="canceled", data=df, ax=ax3)
    plt.title("Cancellation Distribution")
    st.pyplot(fig3)
