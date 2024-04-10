import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Setup for better aesthetics in plots
sns.set_theme(style="whitegrid")

# Simulate fetching sensor data
def generate_sensor_data(num_entries=100):
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=num_entries, freq='T')
    temperatures = np.random.normal(loc=20, scale=5, size=num_entries)  # Normal distribution
    humidity = np.random.uniform(low=30, high=70, size=num_entries)  # Uniform distribution
    sensor_data = pd.DataFrame({'Timestamp': timestamps, 'Temperature': temperatures, 'Humidity': humidity})
    return sensor_data

# Basic anomaly detection for demonstration
def detect_anomalies(dataframe, temp_threshold=25):
    anomalies = dataframe[dataframe['Temperature'] > temp_threshold]
    return anomalies

st.title('Urban Farm Sensor Dashboard')

# Simulate data fetching/loading
with st.spinner('Fetching sensor data...'):
    simulated_data = generate_sensor_data()
    time.sleep(2)  # Simulate delay

# Section: Sensor Data Overview
st.subheader("Sensor Data Overview:")
st.dataframe(simulated_data)

# Section: Basic Statistics
st.subheader("Basic Statistics:")
st.dataframe(simulated_data.describe())

# Section: Anomaly Detection
st.subheader("Anomaly Detection")
anomaly_threshold = st.slider('Set temperature anomaly threshold', min_value=15, max_value=30, value=25)
anomalies = detect_anomalies(simulated_data, temp_threshold=anomaly_threshold)
if not anomalies.empty:
    st.warning(f"Detected Anomalies (Temperature > {anomaly_threshold}°C):")
    st.dataframe(anomalies)
else:
    st.success("No anomalies detected with the current threshold.")

# Visualization section
st.subheader("Visualizations")

# Custom plotting function
def plot_time_series(data, column, title, ylabel):
    fig, ax = plt.subplots()
    sns.lineplot(x=data['Timestamp'], y=data[column], ax=ax)
    ax.set(title=title, xlabel='Time', ylabel=ylabel)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Temperature over time
plot_time_series(simulated_data, 'Temperature', 'Temperature Over Time', 'Temperature (°C)')

# Humidity over time
plot_time_series(simulated_data, 'Humidity', 'Humidity Over Time', 'Humidity (%)')
