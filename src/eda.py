# eda.py: Exploratory Data Analysis script

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import zscore

# Function to load data
def load_data(filepath):
    """Load cleaned air quality data from the specified file path."""
    air_df = pd.read_csv(filepath)
    return air_df

# Function for Univariate Analysis
def univariate_analysis(data, save_path):
    """Perform univariate analysis with histograms, KDE plots, and boxplots."""
    plt.figure(figsize=(20, 15))
    for i, column in enumerate(data.columns):
        plt.subplot(5, 3, i + 1)
        sns.histplot(data[column], kde=True)
        plt.title(f'Distribution of {column}')
    plt.tight_layout()
    plt.savefig(f'{save_path}/univariate_histograms_kde.png')
    plt.show()

    # Boxplots (excluding 'AH' column for separate analysis)
    plt.figure(figsize=(20, 15))
    sns.boxplot(data=data.drop(columns='AH', axis=1))
    plt.title('Box Plots of All Variables except AH')
    plt.xticks(rotation=90)
    plt.savefig(f'{save_path}/boxplots_without_AH.png')
    plt.show()

    # Boxplot for 'AH'
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data['AH'])
    plt.title('Box Plot of AH')
    plt.savefig(f'{save_path}/boxplot_AH.png')
    plt.show()

# Function for Bivariate Analysis
def bivariate_analysis(data, save_path):
    """Perform bivariate analysis with pairplots."""
    sns.pairplot(data, kind='reg', plot_kws={'line_kws': {'color': 'red'}})
    plt.savefig(f'{save_path}/pairwise_relationships.png')
    plt.show()

# Function for Multivariate Analysis
def multivariate_analysis(data, save_path):
    """Perform multivariate analysis with a 3D scatter plot."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['CO(GT)'], data['NOx(GT)'], data['NO2(GT)'])
    ax.set_xlabel('CO(GT)')
    ax.set_ylabel('NOx(GT)')
    ax.set_zlabel('NO2(GT)')
    plt.title('3D Scatter Plot of CO(GT), NOx(GT), and NO2(GT)')
    plt.savefig(f'{save_path}/3d_scatter_plot.png')
    plt.show()

# Function for Time Series Analysis
def time_series_analysis(data, save_path):
    """Perform time series analysis including daily averages and moving averages."""
    # Convert Date and Time to datetime
    data['datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d/%m/%Y %H.%M.%S')
    
    # Set datetime as index and drop original Date and Time columns
    data.set_index('datetime', inplace=True)
    data.drop(['Date', 'Time'], axis=1, inplace=True)

    # Resampling to daily averages
    data_resampled = data.resample('D').mean()

    # Plot time series for each pollutant
    plt.figure(figsize=(14, 8))
    for column in ['CO(GT)', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)', 'NOx(GT)', 'NO2(GT)']:
        plt.plot(data_resampled.index, data_resampled[column], label=column)

    plt.title('Daily Average Concentrations of Pollutants Over Time')
    plt.xlabel('Date')
    plt.ylabel('Concentration')
    plt.legend()
    plt.savefig(f'{save_path}/daily_average_concentrations.png')
    plt.show()

    # Moving Averages
    data_resampled['CO(GT)_MA'] = data_resampled['CO(GT)'].rolling(window=30).mean()
    data_resampled['NOx(GT)_MA'] = data_resampled['NOx(GT)'].rolling(window=30).mean()

    # Plot the moving averages
    plt.figure(figsize=(14, 8))
    plt.plot(data_resampled['CO(GT)_MA'], label='CO(GT) 30-day MA')
    plt.plot(data_resampled['NOx(GT)_MA'], label='NOx(GT) 30-day MA')
    plt.title('30-Day Moving Averages of CO(GT) and NOx(GT)')
    plt.xlabel('Date')
    plt.ylabel('Concentration')
    plt.legend()
    plt.savefig(f'{save_path}/moving_averages.png')
    plt.show()

    return data_resampled

# Function for Seasonal Decomposition
def seasonal_decomposition_analysis(data, column, save_path):
    """Perform seasonal decomposition on the specified column."""
    result = seasonal_decompose(data[column].dropna(), model='additive', period=30)
    result.plot()
    plt.savefig(f'{save_path}/seasonal_decomposition.png')
    plt.show()

# Function for Outlier Detection
def outlier_detection(data):
    """Detect outliers using z-scores."""
    z_scores = data.apply(zscore)
    outliers = (z_scores.abs() > 3).sum()
    print(f'Percentage of outliers: {outliers / data.shape[0] * 100:.2f}%')

# Main function to run all analyses
def perform_eda(filepath, save_path):
    """Perform full exploratory data analysis (EDA) on the dataset."""
    # Load data
    air_df = load_data(filepath)

    # Univariate analysis
    print("Performing Univariate Analysis...")
    univariate_analysis(air_df, save_path)

    # Bivariate analysis
    print("Performing Bivariate Analysis...")
    bivariate_analysis(air_df, save_path)

    # Multivariate analysis
    print("Performing Multivariate Analysis...")
    multivariate_analysis(air_df, save_path)

    # Time series analysis
    print("Performing Time Series Analysis...")
    air_df_resampled = time_series_analysis(air_df, save_path)

    # Seasonal decomposition
    print("Performing Seasonal Decomposition Analysis...")
    seasonal_decomposition_analysis(air_df_resampled, 'CO(GT)', save_path)

    # Outlier detection
    print("Performing Outlier Detection...")
    outlier_detection(air_df)

# Run EDA script if executed as the main script
if __name__ == "__main__":
    perform_eda(filepath='../data/processed/air_cleaned.csv', save_path='../reports/figures')