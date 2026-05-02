import streamlit as st
import pandas as pd

# PAGE CONFIG
st.set_page_config(layout="wide")

# TITLE
st.title("📊 Supply Chain Profitability Dashboard")

# LOAD DATA FROM GOOGLE DRIVE
df = pd.read_csv(
    "https://drive.google.com/uc?id=1f0j3rAfy4K0HEawz5v9qHDUuK7vOtlsA",
    encoding='latin1',
    engine='python',
    on_bad_lines='skip'
)

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip()

# SAFE TYPE CONVERSION (VERY IMPORTANT)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Order Profit Per Order'] = pd.to_numeric(df['Order Profit Per Order'], errors='coerce')
df['Order Item Discount Rate'] = pd.to_numeric(df['Order Item Discount Rate'], errors='coerce')

# DROP NULL VALUES (FOR STABILITY)
df = df.dropna(subset=['Sales', 'Order Profit Per Order'])

# KPIs
st.subheader("📌 Key Metrics")
col1, col2 = st.columns(2)

col1.metric("Total Revenue", f"${round(df['Sales'].sum(), 2):,}")
col2.metric("Total Profit", f"${round(df['Order Profit Per Order'].sum(), 2):,}")

# PROFIT MARGIN
df['Profit Margin'] = df['Order Profit Per Order'] / df['Sales']

# SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")

segment = st.sidebar.selectbox(
    "Customer Segment",
    sorted(df['Customer Segment'].dropna().unique())
)

region = st.sidebar.selectbox(
    "Order Region",
    sorted(df['Order Region'].dropna().unique())
)

# FILTER DATA
filtered_df = df[
    (df['Customer Segment'] == segment) &
    (df['Order Region'] == region)
]

# CHARTS

# 1. Profit by Category
st.subheader("📦 Profit by Category")
category_profit = filtered_df.groupby('Category Name')['Order Profit Per Order'].sum().sort_values()
st.bar_chart(category_profit)

# 2. Top Customers
st.subheader("👤 Top Customers by Profit")
top_customers = filtered_df.groupby('Customer Id')['Order Profit Per Order'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_customers)

# 3. Discount vs Profit
st.subheader("🎯 Discount vs Profit")
st.scatter_chart(filtered_df[['Order Item Discount Rate', 'Order Profit Per Order']].dropna())

# 4. Profit by Region (Overall)
st.subheader("🌍 Profit by Region")
region_profit = df.groupby('Order Region')['Order Profit Per Order'].sum()
st.bar_chart(region_profit)
