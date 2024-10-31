# eda.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_corr_matrix(df):
    """Plot the correlation matrix."""
    plt.figure(figsize=(10, 8))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

def plot_pollutant_distribution(df, pollutant_column):
    """Plot distribution of a specified pollutant."""
    sns.histplot(df[pollutant_column], kde=True, color='blue')
    plt.title(f'Distribution of {pollutant_column}')
    plt.xlabel(f'{pollutant_column}')
    plt.ylabel('Frequency')
    plt.show()

def eda_pipeline(filepath):
    """Run the EDA pipeline on the dataset."""
    df = pd.read_csv(filepath)
    plot_corr_matrix(df)
    plot_pollutant_distribution(df, 'CO(GT)')

# Example usage
if __name__ == "__main__":
    eda_pipeline("../data/processed/air_quality_cleaned.csv")