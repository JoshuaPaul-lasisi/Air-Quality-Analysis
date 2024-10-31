# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data with datetime
def load_data(filepath):
    """Load the air quality data and set datetime index."""
    df = pd.read_csv(filepath)
    
    # Ensure datetime is properly formatted and set as index if it's not already
    if 'datetime' not in df.columns:
        df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S')
        df.set_index('datetime', inplace=True)
    else:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        
    return df

def plot_pollutant(df, pollutant, start_time, end_time):
    """Plot pollutant data over the specified time range."""
    filtered_df = df.loc[start_time:end_time]
    fig = px.line(filtered_df, x=filtered_df.index, y=pollutant, title=f'Time Series of {pollutant}')
    st.plotly_chart(fig)

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

if __name__ == "__main__":
    main()