import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("DATA.csv")

# Page title
st.set_page_config(layout="wide")
st.title("📊 Sales and Marketing Insights Dashboard")
st.markdown("""
This dashboard provides comprehensive insights into the entire customer journey—from acquisition to sales.
Use the filters on the sidebar to slice and dice your data.
""")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
# Update these columns based on your dataset columns
regions = st.sidebar.multiselect("Select Region(s)", options=df["Region"].unique(), default=df["Region"].unique())
products = st.sidebar.multiselect("Select Product(s)", options=df["Product"].unique(), default=df["Product"].unique())
channels = st.sidebar.multiselect("Select Channel(s)", options=df["Channel"].unique(), default=df["Channel"].unique())
date_range = st.sidebar.date_input("Select Date Range", [])

# Filter data
filtered_df = df[df["Region"].isin(regions) & df["Product"].isin(products) & df["Channel"].isin(channels)]
if date_range:
    filtered_df = filtered_df[(pd.to_datetime(filtered_df["Date"]) >= pd.to_datetime(date_range[0])) & 
                              (pd.to_datetime(filtered_df["Date"]) <= pd.to_datetime(date_range[1]))]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "🛒 Product Analysis",
    "🌍 Regional Insights",
    "🧭 Advanced Metrics"
])

# Overview Tab
with tab1:
    st.header("📈 Overall Trends")
    
    st.markdown("**1️⃣ Sales Over Time**\nThis line chart shows total sales over time.")
    fig1 = px.line(filtered_df.groupby("Date")["Sales"].sum().reset_index(), x="Date", y="Sales", title="Sales Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("**2️⃣ Leads vs Conversions per Channel**\nSee which channels drive conversions.")
    fig2 = px.bar(filtered_df.groupby("Channel")[["Leads", "Conversions"]].sum().reset_index(), 
                  x="Channel", y=["Leads", "Conversions"], barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**3️⃣ Sales Distribution**\nDistribution of sales values.")
    fig3 = px.histogram(filtered_df, x="Sales", nbins=30)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**4️⃣ Correlation Heatmap**\nRelationships between numeric metrics.")
    corr = filtered_df[["Sales", "Marketing_Spend", "Leads", "Conversions"]].corr()
    st.dataframe(corr)

    st.markdown("**5️⃣ Top Transactions**\nTop 10 sales records.")
    st.dataframe(filtered_df.sort_values("Sales", ascending=False).head(10))

# Product Analysis Tab
with tab2:
    st.header("🛒 Product Performance")
    
    st.markdown("**6️⃣ Sales by Product**\nTotal sales by each product.")
    fig4 = px.bar(filtered_df.groupby("Product")["Sales"].sum().reset_index(), x="Product", y="Sales")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**7️⃣ Average Conversions per Product**\nWhich products convert best?")
    fig5 = px.bar(filtered_df.groupby("Product")["Conversions"].mean().reset_index(), x="Product", y="Conversions")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("**8️⃣ Marketing Spend vs Sales (Scatter)**\nHow marketing spend relates to sales.")
    fig6 = px.scatter(filtered_df, x="Marketing_Spend", y="Sales", color="Product", size="Conversions")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("**9️⃣ Leads per Product**\nLead generation by product.")
    fig7 = px.bar(filtered_df.groupby("Product")["Leads"].sum().reset_index(), x="Product", y="Leads")
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("**🔟 Conversion Rate per Product**\nConversions divided by leads.")
    df["Conversion_Rate"] = df["Conversions"] / df["Leads"]
    fig8 = px.bar(df.groupby("Product")["Conversion_Rate"].mean().reset_index(), x="Product", y="Conversion_Rate")
    st.plotly_chart(fig8, use_container_width=True)

# Regional Insights Tab
with tab3:
    st.header("🌍 Regional Performance")

    st.markdown("**11️⃣ Sales by Region**\nOverall sales by region.")
    fig9 = px.pie(filtered_df, names="Region", values="Sales")
    st.plotly_chart(fig9, use_container_width=True)

    st.markdown("**12️⃣ Sales Trend per Region**\nMonthly sales trends split by region.")
    fig10 = px.line(filtered_df.groupby(["Date", "Region"])["Sales"].sum().reset_index(), x="Date", y="Sales", color="Region")
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown("**13️⃣ Leads vs Conversions per Region**\nRegional conversion performance.")
    fig11 = px.bar(filtered_df.groupby("Region")[["Leads", "Conversions"]].sum().reset_index(), x="Region", y=["Leads", "Conversions"], barmode="group")
    st.plotly_chart(fig11, use_container_width=True)

    st.markdown("**14️⃣ Average Sales per Transaction by Region**")
    fig12 = px.bar(filtered_df.groupby("Region")["Sales"].mean().reset_index(), x="Region", y="Sales")
    st.plotly_chart(fig12, use_container_width=True)

# Advanced Metrics Tab
with tab4:
    st.header("🧭 Advanced Metrics")

    st.markdown("**15️⃣ Sales vs Leads Scatter Plot**\nDo more leads correlate to more sales?")
    fig13 = px.scatter(filtered_df, x="Leads", y="Sales", color="Region")
    st.plotly_chart(fig13, use_container_width=True)

    st.markdown("**16️⃣ Sales vs Conversions Scatter Plot**")
    fig14 = px.scatter(filtered_df, x="Conversions", y="Sales", color="Region")
    st.plotly_chart(fig14, use_container_width=True)

    st.markdown("**17️⃣ Sales per Customer Segment**")
    fig15 = px.bar(filtered_df.groupby("Customer_Segment")["Sales"].sum().reset_index(), x="Customer_Segment", y="Sales")
    st.plotly_chart(fig15, use_container_width=True)

    st.markdown("**18️⃣ Marketing Spend by Channel**")
    fig16 = px.bar(filtered_df.groupby("Channel")["Marketing_Spend"].sum().reset_index(), x="Channel", y="Marketing_Spend")
    st.plotly_chart(fig16, use_container_width=True)

    st.markdown("**19️⃣ Conversion Rate by Channel**")
    fig17 = px.bar(df.groupby("Channel")["Conversion_Rate"].mean().reset_index(), x="Channel", y="Conversion_Rate")
    st.plotly_chart(fig17, use_container_width=True)

    st.markdown("**20️⃣ Sales Distribution by Month**")
    filtered_df["Month"] = pd.to_datetime(filtered_df["Date"]).dt.month
    fig18 = px.box(filtered_df, x="Month", y="Sales")
    st.plotly_chart(fig18, use_container_width=True)
