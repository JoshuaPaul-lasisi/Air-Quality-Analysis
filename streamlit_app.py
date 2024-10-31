# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
def load_data(filepath):
    """Load the air quality data."""
    return pd.read_csv(filepath)

def plot_pollutant(df, pollutant, time_range):
    """Plot pollutant data over the specified time range."""
    filtered_df = df.iloc[:time_range]
    fig = px.line(filtered_df, x=filtered_df.index, y=pollutant, title=f'Time Series of {pollutant}')
    st.plotly_chart(fig)

# Streamlit app
def main():
    st.title("Air Quality Dashboard with Streamlit")

    # Load data
    data = load_data("../data/processed/air_quality_cleaned.csv")

    # Dropdown to select pollutant
    pollutant = st.selectbox('Select a Pollutant:', ['CO(GT)', 'NOx(GT)', 'NO2(GT)'], index=0)

    # Slider for time range
    time_range = st.slider("Select Time Range:", min_value=0, max_value=len(data), value=len(data) // 2)

    # Plot the selected pollutant
    plot_pollutant(data, pollutant, time_range)

if __name__ == "__main__":
    main()