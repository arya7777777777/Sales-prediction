import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the page
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales and Marketing Insights Dashboard")
st.markdown("""
This dashboard offers an end-to-end view of your sales pipeline—from customer acquisition to conversion.
Use the sidebar filters to customize the analysis.
""")

# Load CSV with encoding handling
try:
    df = pd.read_csv("DATA.csv", encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv("DATA.csv", encoding="ISO-8859-1")

# Show raw data preview
if st.checkbox("Show raw data"):
    st.write(df.head())

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Check and prepare filter options safely
regions = df["Region"].dropna().unique().tolist() if "Region" in df.columns else []
products = df["Product"].dropna().unique().tolist() if "Product" in df.columns else []
channels = df["Channel"].dropna().unique().tolist() if "Channel" in df.columns else []

if regions:
    selected_regions = st.sidebar.multiselect("Select Region(s):", regions, default=regions)
else:
    selected_regions = []

if products:
    selected_products = st.sidebar.multiselect("Select Product(s):", products, default=products)
else:
    selected_products = []

if channels:
    selected_channels = st.sidebar.multiselect("Select Channel(s):", channels, default=channels)
else:
    selected_channels = []

# Date filtering if Date column exists
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date])
else:
    date_range = []

# Apply filters
filtered_df = df.copy()

if selected_regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
if selected_products:
    filtered_df = filtered_df[filtered_df["Product"].isin(selected_products)]
if selected_channels:
    filtered_df = filtered_df[filtered_df["Channel"].isin(selected_channels)]
if date_range and len(date_range) == 2 and "Date" in df.columns:
    filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(date_range[0])) & (filtered_df["Date"] <= pd.to_datetime(date_range[1]))]

# Tabs for clarity
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "🛒 Product Analysis",
    "🌍 Regional Insights",
    "🧭 Advanced Metrics"
])

# Overview Tab
with tab1:
    st.header("Overall Sales Trends")

    if "Date" in df.columns and "Sales" in df.columns:
        st.markdown("**1️⃣ Sales Over Time**")
        sales_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()
        fig = px.line(sales_trend, x="Date", y="Sales")
        st.plotly_chart(fig, use_container_width=True)

    if "Channel" in df.columns and "Leads" in df.columns and "Conversions" in df.columns:
        st.markdown("**2️⃣ Leads vs Conversions per Channel**")
        channel_data = filtered_df.groupby("Channel")[["Leads", "Conversions"]].sum().reset_index()
        fig = px.bar(channel_data, x="Channel", y=["Leads", "Conversions"], barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    if "Sales" in df.columns:
        st.markdown("**3️⃣ Sales Distribution Histogram**")
        fig = px.histogram(filtered_df, x="Sales", nbins=30)
        st.plotly_chart(fig, use_container_width=True)

# Product Analysis Tab
with tab2:
    st.header("Product Performance")

    if "Product" in df.columns and "Sales" in df.columns:
        st.markdown("**4️⃣ Total Sales by Product**")
        fig = px.bar(filtered_df.groupby("Product")["Sales"].sum().reset_index(), x="Product", y="Sales")
        st.plotly_chart(fig, use_container_width=True)

    if "Product" in df.columns and "Conversions" in df.columns:
        st.markdown("**5️⃣ Average Conversions per Product**")
        fig = px.bar(filtered_df.groupby("Product")["Conversions"].mean().reset_index(), x="Product", y="Conversions")
        st.plotly_chart(fig, use_container_width=True)

    if "Marketing_Spend" in df.columns and "Sales" in df.columns and "Product" in df.columns:
        st.markdown("**6️⃣ Marketing Spend vs Sales Scatter**")
        fig = px.scatter(filtered_df, x="Marketing_Spend", y="Sales", color="Product", size="Conversions")
        st.plotly_chart(fig, use_container_width=True)

# Regional Insights Tab
with tab3:
    st.header("Regional Performance")

    if "Region" in df.columns and "Sales" in df.columns:
        st.markdown("**7️⃣ Sales by Region Pie Chart**")
        fig = px.pie(filtered_df, names="Region", values="Sales")
        st.plotly_chart(fig, use_container_width=True)

    if "Date" in df.columns and "Region" in df.columns and "Sales" in df.columns:
        st.markdown("**8️⃣ Sales Trend per Region**")
        trend = filtered_df.groupby(["Date", "Region"])["Sales"].sum().reset_index()
        fig = px.line(trend, x="Date", y="Sales", color="Region")
        st.plotly_chart(fig, use_container_width=True)

# Advanced Metrics Tab
with tab4:
    st.header("Advanced Metrics")

    if "Leads" in df.columns and "Sales" in df.columns and "Region" in df.columns:
        st.markdown("**9️⃣ Sales vs Leads Scatter Plot**")
        fig = px.scatter(filtered_df, x="Leads", y="Sales", color="Region")
        st.plotly_chart(fig, use_container_width=True)

    if "Conversions" in df.columns and "Sales" in df.columns and "Region" in df.columns:
        st.markdown("**🔟 Sales vs Conversions Scatter Plot**")
        fig = px.scatter(filtered_df, x="Conversions", y="Sales", color="Region")
        st.plotly_chart(fig, use_container_width=True)

    if "Customer_Segment" in df.columns and "Sales" in df.columns:
        st.markdown("**11️⃣ Sales per Customer Segment**")
        fig = px.bar(filtered_df.groupby("Customer_Segment")["Sales"].sum().reset_index(), x="Customer_Segment", y="Sales")
        st.plotly_chart(fig, use_container_width=True)

# Data Table
st.header("📋 Data Table of Filtered Results")
st.dataframe(filtered_df)

st.markdown("""
---
✅ **Tip:** Use the filters to narrow down the data for more focused analysis.
""")
