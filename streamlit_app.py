import streamlit as st
import pandas as pd
import plotly.express as px
import pmdarima as pm
from datetime import datetime
import matplotlib.pyplot as plt

# Load data with datetime
def load_data(filepath):
    """Load the air quality data and set datetime index."""
    df = pd.read_csv(filepath)
    
    # Ensure datetime is properly formatted and set as index if it's not already
    if 'datetime' not in df.columns:
        df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
        df.set_index('datetime', inplace=True)
    else:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        df.set_index('datetime', inplace=True)
    
    # Convert pollutant columns to numeric, forcing non-numeric values to NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    return df

def plot_pollutant(df, pollutant, start_time, end_time):
    """Plot pollutant data over the specified time range."""
    filtered_df = df.loc[start_time:end_time]
    fig = px.line(filtered_df, x=filtered_df.index, y=pollutant, title=f'Time Series of {pollutant}')
    st.plotly_chart(fig)

def plot_seasonal_trends(df, pollutant, freq='ME'):
    resampled_data = df[pollutant].resample(freq).mean()
    fig = px.line(resampled_data, title=f'{pollutant} - Seasonal Trend')
    st.plotly_chart(fig)

def pollutant_forecast(df, pollutant, steps=30):
    model = pm.auto_arima(df[pollutant], seasonal=True, m=12)
    forecast = model.predict(n_periods=steps)
    future_dates = pd.date_range(df.index[-1], periods=steps + 1, freq='D')[1:]
    forecast_df = pd.DataFrame(forecast, index=future_dates, columns=[pollutant])

    plt.figure(figsize=(10, 4))
    plt.plot(df[pollutant], label='Historical Data')
    plt.plot(forecast_df, label='Forecast')
    plt.legend()
    st.pyplot(plt)

def health_risk_alert(pollutant_level, threshold):
    if pollutant_level > threshold:
        st.warning(f"Warning: {pollutant_level} exceeds safe threshold of {threshold}")
    else:
        st.success(f"Safe Level: {pollutant_level}")

def check_custom_alert(pollutant_level, threshold):
    if pollutant_level > threshold:
        st.warning(f"Alert: {pollutant_level} exceeds your custom threshold of {threshold}")
    else:
        st.info(f"Current level: {pollutant_level}")

# Streamlit app
def main():
    st.title("Air Quality Dashboard")

    # Load data
    data = load_data("./data/processed/air_cleaned.csv")

    # Dropdown to select pollutant
    pollutant = st.selectbox('Select a Pollutant:', ['CO(GT)', 'NOx(GT)', 'NO2(GT)'], index=0)

    # Convert to Python datetime for Streamlit slider
    min_time = data.index.min().to_pydatetime()
    max_time = data.index.max().to_pydatetime()

    # Select time range
    start_time = st.slider("Select Start Time:", min_value=min_time, max_value=max_time, value=min_time, format="YYYY-MM-DD HH:mm")
    end_time = st.slider("Select End Time:", min_value=min_time, max_value=max_time, value=max_time, format="YYYY-MM-DD HH:mm")

    # Plot the selected pollutant
    plot_pollutant(data, pollutant, start_time, end_time)
    
    # Frequency selection for seasonal trends
    st.subheader("Seasonal Trends and Anomalies")
    frequency = st.radio("Select Frequency", ['Daily', 'Weekly', 'Monthly'])
    freq_dict = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'M'}
    plot_seasonal_trends(data, pollutant, freq=freq_dict[frequency])
    
    # Pollutant Forecasting
    st.subheader("Pollutant Forecasting")
    steps = st.slider("Days to Forecast", 1, 90, 30)
    pollutant_forecast(data, pollutant, steps)
    
    # Health Risk Levels
    st.subheader("Health Risk Levels")
    thresholds = {'CO(GT)': 5, 'NOx(GT)': 10} # Sample thresholds
    current_level = data[pollutant].iloc[-1]
    health_risk_alert(current_level, thresholds[pollutant])
    
    # User-Defined Alerts
    st.subheader("User-Defined Alerts")
    custom_threshold = st.slider("Set Custom Threshold", min_value=float(data[pollutant].min()), max_value=float(data[pollutant].max()))
    check_custom_alert(data[pollutant].iloc[-1], custom_threshold)

if __name__ == "__main__":
    main()