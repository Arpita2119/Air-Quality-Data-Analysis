"""
Air Quality Dashboard

This Streamlit app visualizes air pollution trends across major Indian cities.
Features:
- City-wise average pollution levels
- Monthly and yearly trends
- Time-series plots
- Health risk categorization based on PM2.5 levels

Author: Arpita Garg
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Title
st.title("📊 Air Quality Dashboard - India")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("city_day.csv", parse_dates=["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
cities = sorted(df["City"].dropna().unique())
selected_city = st.sidebar.selectbox("Select a City", cities)

pollutants = ["PM2.5", "PM10", "NO", "NO2"]
selected_pollutant = st.sidebar.selectbox("Select Pollutant", pollutants)

years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

# Filter Data
filtered_df = df[(df["City"] == selected_city) & (df["Year"] == selected_year)]

# Check if data is available
if filtered_df.empty:
    st.warning("No data available for this selection.")
    st.stop()

# Monthly average for selected pollutant
monthly_avg = (
    filtered_df.groupby("Month")[selected_pollutant]
    .mean()
    .reset_index()
)

# Display key metrics
st.subheader(f"📍 City: {selected_city} | 🧪 Pollutant: {selected_pollutant} | 📅 Year: {selected_year}")
st.metric("Annual Average", f"{filtered_df[selected_pollutant].mean():.2f} µg/m³")
st.metric("Max Monthly Avg", f"{monthly_avg[selected_pollutant].max():.2f} µg/m³")

# Plot line chart
st.subheader("📈 Monthly Average Levels")
fig, ax = plt.subplots()
sns.lineplot(data=monthly_avg, x="Month", y=selected_pollutant, marker="o", ax=ax)
ax.set_title(f"{selected_pollutant} Trend in {selected_city} ({selected_year})")
ax.set_ylabel(f"{selected_pollutant} (µg/m³)")
ax.set_xlabel("Month")
st.pyplot(fig)

# Show monthly data
st.subheader("🗃️ Monthly Average Data")
st.dataframe(monthly_avg.style.background_gradient(cmap="Blues"))

# Optional: Health Risk Category (for PM2.5)
if selected_pollutant == "PM2.5":
    st.subheader("⚠️ PM2.5 Health Risk Classification")
    def classify_pm25(val):
        if val <= 30:
            return "Good"
        elif val <= 60:
            return "Moderate"
        elif val <= 90:
            return "Poor"
        elif val <= 120:
            return "Very Poor"
        else:
            return "Severe"
    monthly_avg["Health Risk"] = monthly_avg["PM2.5"].apply(classify_pm25)
    st.dataframe(monthly_avg[["Month", "PM2.5", "Health Risk"]])

# Footer
st.markdown("---")
st.markdown("Built by Arpita Garg | Data source: [Kaggle - Air Quality India](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)")
