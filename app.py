import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Project Profitability Analyzer", layout="wide")
st.title("📊 Project Profitability Analyzer")

# Load data
file_path = "dataa/Project_Profitability_Tracker_100.csv"


df = pd.read_csv(file_path)

# Data cleaning & feature engineering
# Data cleaning & feature engineering
df['Start_Date'] = pd.to_datetime(df['Start_Date'], dayfirst=True)
df['End_Date'] = pd.to_datetime(df['End_Date'], dayfirst=True)


df['Profit'] = df['Revenue'] - df['Cost']
df['ROI'] = (df['Profit'] / df['Cost']) * 100
df['Duration'] = (df['End_Date'] - df['Start_Date']).dt.days
df['Month'] = df['Start_Date'].dt.to_period('M').astype(str)
df['Status'] = df['Profit'].apply(lambda x: 'Profit' if x >= 0 else 'Loss')

# Sidebar filters
st.sidebar.header("🔍 Filters")

client = st.sidebar.selectbox(
    "Select Client",
    ["All"] + sorted(df['Client'].unique())
)

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df['Month'].unique())
)

status = st.sidebar.radio(
    "Project Status",
    ["All", "Profit", "Loss"]
)

# Apply filters
filtered_df = df.copy()

if client != "All":
    filtered_df = filtered_df[filtered_df['Client'] == client]

if month != "All":
    filtered_df = filtered_df[filtered_df['Month'] == month]

if status != "All":
    filtered_df = filtered_df[filtered_df['Status'] == status]

# KPIs
st.subheader("📌 Key Metrics")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Projects", len(filtered_df))
c2.metric("Total Profit", f"₹{filtered_df['Profit'].sum():,.0f}")
c3.metric("Avg ROI", f"{filtered_df['ROI'].mean():.2f}%")
c4.metric("Avg Duration", f"{filtered_df['Duration'].mean():.0f} days")

# Monthly Profit Chart
st.subheader("📈 Monthly Profit Trend")
monthly = filtered_df.groupby('Month')['Profit'].sum().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=monthly, x='Month', y='Profit', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# Profit vs Loss Pie Chart
st.subheader("🥧 Profit vs Loss Distribution")
status_count = filtered_df['Status'].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(
    status_count,
    labels=status_count.index,
    autopct='%1.1f%%',
    startangle=90
)
ax2.axis('equal')
st.pyplot(fig2)

# Top Clients
st.subheader("🏆 Top Clients by Profit")
top_clients = filtered_df.groupby('Client')['Profit'].sum().sort_values(ascending=False).head(5)
st.dataframe(top_clients.reset_index())

st.success("✅ Dashboard Loaded Successfully")
