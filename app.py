import sys
import types
sys.modules['pyarrow'] = types.ModuleType('pyarrow')
sys.modules['pyarrow'].__version__ = '25.0.0'
import sys
sys.modules['pyarrow'] = type('sys', (), {'__version__': '25.0.0'})
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configure browser tab properties
st.set_page_config(page_title="Enterprise Retail Analytics", page_icon="📈", layout="wide")

st.title("📊 Enterprise E-Commerce Analytics Platform")
st.markdown("---")

# 2. Optimized Data Loading with Cache memory
@st.cache_data
def load_clean_data():
    df = pd.read_csv("data/cleaned_ecommerce_sales.csv")
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

df = load_clean_data()

# 3. Interactive Sidebar Filters
st.sidebar.header("🕹️ Control Panel Filters")
available_countries = sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("Select Target Region/Country", ["All Countries"] + available_countries)

# Apply filter instantly based on user interaction in browser
if selected_country != "All Countries":
    filtered_df = df[df['Country'] == selected_country]
else:
    filtered_df = df

# 4. Executive KPI Metric Cards Dashboard
st.subheader("📌 Key Performance Indicators (KPIs)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_revenue = filtered_df['Revenue'].sum()
total_orders = filtered_df['InvoiceDate'].nunique()
unique_buyers = filtered_df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

kpi1.metric("Gross Revenue", f"${total_revenue:,.2f}")
kpi2.metric("Total Order Count", f"{total_orders:,}")
kpi3.metric("Active Customer Base", f"{unique_buyers:,}")
kpi4.metric("Avg Order Value (AOV)", f"${avg_order_value:,.2f}")

st.markdown("---")

# 5. Visual Layout Split
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🛒 Top 10 High-Revenue Generating Products")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    top_prod = filtered_df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    sns.barplot(data=top_prod, x='Revenue', y='Description', hue='Description', palette='Blues_r', legend=False, ax=ax1)
    ax1.set_xlabel("Total Sales Revenue ($)")
    ax1.set_ylabel("")
    st.pyplot(fig1)

with col_right:
    st.subheader("🕒 Operational Customer Traffic Hourly Matrix")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # Derive hour tracking cleanly
    filtered_df['HourOfDay'] = pd.to_datetime(filtered_df['InvoiceDate']).dt.hour
    hourly_traffic = filtered_df.groupby('HourOfDay')['Revenue'].count().reset_index(name='Orders')
        
    sns.lineplot(data=hourly_traffic, x='HourOfDay', y='Orders', marker='o', color='#1E3A8A', linewidth=2.5, ax=ax2)
    ax2.set_xlabel("Hour of the Day (24hr clock)")
    ax2.set_ylabel("Transaction Count")
    ax2.set_xticks(range(6, 21))
    st.pyplot(fig2)
