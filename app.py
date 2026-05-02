import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv(
    "APL_Logistics1.csv",
    encoding='latin1',
    engine='python',
    on_bad_lines='skip'
)

# Title
st.title("📊 Supply Chain Profitability Dashboard")

# KPIs
st.subheader("Key Metrics")
col1, col2 = st.columns(2)

col1.metric("Total Revenue", round(df['Sales'].sum(), 2))
col2.metric("Total Profit", round(df['Order Profit Per Order'].sum(), 2))

# Profit Margin
df['Profit Margin'] = df['Order Profit Per Order'] / df['Sales']

# Filters
st.sidebar.header("Filters")

segment = st.sidebar.selectbox(
    "Customer Segment",
    df['Customer Segment'].unique()
)

region = st.sidebar.selectbox(
    "Order Region",
    df['Order Region'].unique()
)

filtered_df = df[
    (df['Customer Segment'] == segment) &
    (df['Order Region'] == region)
]

# Charts
st.subheader("📦 Profit by Category")
st.bar_chart(filtered_df.groupby('Category Name')['Order Profit Per Order'].sum())

st.subheader("👤 Top Customers by Profit")
top_customers = filtered_df.groupby('Customer Id')['Order Profit Per Order'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_customers)

st.subheader("🎯 Discount vs Profit")
st.scatter_chart(filtered_df[['Order Item Discount Rate', 'Order Profit Per Order']])

st.subheader("🌍 Profit by Region")
st.bar_chart(df.groupby('Order Region')['Order Profit Per Order'].sum())
