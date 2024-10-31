# data_preprocessing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    """Loads the dataset from a specified filepath."""
    return pd.read_csv(filepath)

def handle_missing_values(df):
    """Imputes missing values in the dataset with median values."""
    return df.fillna(df.median())

def create_pollution_index(df):
    """Create a new feature 'pollution_index' as the average of key pollutants."""
    df['pollution_index'] = df[['CO(GT)', 'NOx(GT)', 'NO2(GT)']].mean(axis=1)
    return df

def scale_features(df):
    """Scale numerical features using StandardScaler."""
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return scaled_data

def data_preprocessing_pipeline(filepath):
    """Pipeline to handle data loading, missing values, feature creation, and scaling."""
    df = load_data(filepath)
    df = handle_missing_values(df)
    df = create_pollution_index(df)
    df = scale_features(df)
    return df

# Example usage
if __name__ == "__main__":
    processed_data = data_preprocessing_pipeline("../data/raw/air_quality.csv")
    print(processed_data.head())