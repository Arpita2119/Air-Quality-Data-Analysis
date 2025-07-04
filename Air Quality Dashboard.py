"""
Air Quality Dashboard

This Streamlit app visualizes air pollution trends across major Indian cities.
Features:
- City-wise average pollution levels
- Monthly and yearly trends
- Time-series forecasting (PM2.5)
- Health risk categorization based on PM2.5 levels

Built as part of a data analysis project using public air quality data.

Author: [Your Name]
Date: [Date]
"""
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title for the app
st.title("📊 Air Quality Dashboard")

# Load your CSV file
df = pd.read_csv("city_day.csv", parse_dates=["Date"])

# Create Year and Month columns
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# Dropdown for City selection
cities = sorted(df["City"].dropna().unique())
selected_city = st.selectbox("Select a City", cities)

# Filter the DataFrame
filtered_df = df[df["City"] == selected_city]

# Dropdown for selecting pollutant
pollutants = ["PM2.5", "PM10", "NO", "NO2"]
selected_pollutant = st.selectbox("Select Pollutant", pollutants)

# Group data by month
monthly_avg = (
    filtered_df
    .groupby("Month")[selected_pollutant]
    .mean()
    .reset_index()
)

# Plot
fig, ax = plt.subplots()
sns.lineplot(data=monthly_avg, x="Month", y=selected_pollutant, marker="o", ax=ax)
ax.set_title(f"Average Monthly {selected_pollutant} in {selected_city}")
st.pyplot(fig)

# Show data table
st.write("Monthly Average Data:", monthly_avg)
