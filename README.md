# Air Quality Dashboard Project

This project is an interactive air quality dashboard that visualizes air pollution data, seasonal trends, forecasts, and health risk levels for various pollutants. Designed with **Dash** and **Streamlit**, this dashboard allows users to explore historical data, monitor real-time air quality levels, and receive health risk alerts. The project aims to provide insightful data visualizations to support better understanding and monitoring of air quality.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Data Source](#data-source)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)

## Project Overview

Air quality monitoring is crucial for health, environment, and policy. This project uses air pollution data to provide interactive visualizations and insights into pollutant levels, seasonal trends, and future predictions. By selecting pollutants like **CO**, **NOx**, and **NO₂**, users can explore time series data, set custom health thresholds, and view forecasts. The project offers both **Dash** and **Streamlit** implementations for enhanced flexibility and usability.

## Features

### Key Features

- **Dynamic Data Visualization**: Interactive time-series plots for pollutants with options to customize date ranges.
- **Seasonal Trends**: Monthly, weekly, or daily views of pollutant data to identify seasonal patterns.
- **Pollutant Forecasting**: 1 to 90-day forecast using time series analysis for future pollutant levels.
- **Health Risk Alerts**: Notifications for pollutant levels that exceed predefined or user-defined thresholds.
- **Customizable User Alerts**: Adjustable thresholds to receive alerts tailored to user preferences.

### Dash vs. Streamlit Comparison

| Feature                    | Dash                      | Streamlit                       |
|----------------------------|---------------------------|---------------------------------|
| Pollutant Selection        | Dropdown Menu             | Dropdown Menu                   |
| Time Range Selection       | Slider                    | Date Slider                     |
| Seasonal Trend Frequency   | Not Available             | Daily/Weekly/Monthly            |
| Forecasting                | Not Available             | 1-90 Day Forecasting with ARIMA |
| Health Risk & Custom Alerts | Basic                     | Configurable Thresholds         |

## Installation

To set up the project, clone the repository and install the necessary packages:

```bash
git clone https://github.com/yourusername/air-quality-dashboard.git
cd air-quality-dashboard
pip install -r requirements.txt
```

## Required Libraries:

```bash
pandas
plotly
dash
streamlit
pmdarima
```
## Usage
Running the Dash App
To run the Dash app:

```bash
python dashboard.py
```
Then open http://localhost:8050 in your browser.

Running the Streamlit App
To run the Streamlit app:

```bash

streamlit run streamlit.py
```
Access the app through the provided Streamlit URL.

## Data Source
The dataset used in this project includes air quality measurements for pollutants such as CO, NOx, and NO₂, with datetime information for historical analysis. Data should be preprocessed and saved in ./data/processed/air_cleaned.csv.

Columns Expected:

datetime: Timestamp of the measurement
CO(GT): Carbon Monoxide levels
NOx(GT): Nitrogen Oxides levels
NO2(GT): Nitrogen Dioxide levels
(Other pollutant columns as needed)

## Future Improvements
Some ideas to further improve the dashboard:

Add more pollutants and data sources for a comprehensive view.
Integrate real-time data APIs for continuous updates.
Implement advanced forecasting models beyond ARIMA.
Enable comparison between cities or regions.

## Contributors
Joshua Paul-lasisi - Developer

Feel free to raise issues or submit pull requests for any suggestions or improvements!
