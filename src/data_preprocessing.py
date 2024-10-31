import pandas as pd
import numpy as np
import os

def clean_air_quality_data(input_file, output_file):
    # Load the data
    air = pd.read_csv(input_file)
    
    # Data Cleaning
    # Drop rows with missing values
    air.dropna(inplace=True)

    # Columns to check for negative values
    columns_to_check = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'C6H6(GT)', 
                        'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 
                        'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 
                        'T', 'RH', 'AH']

    # Replace negative values with NaN
    air[air[columns_to_check] < 0] = np.nan

    # Drop columns with more than 50% missing values
    air.dropna(thresh=len(air) * 0.5, axis=1, inplace=True)

    # Interpolate missing values in numeric columns
    air_numeric_columns = air.select_dtypes(include=['number']).columns
    air_numeric_interpolated = air[air_numeric_columns].interpolate(method='linear', limit_direction='forward')

    # Forward and backward fill remaining NaN values
    air_numeric_interpolated = air_numeric_interpolated.ffill().bfill()

    # Join interpolated data with non-numeric columns
    non_numeric_columns = air.select_dtypes(exclude=['number']).columns
    air_cleaned = air[non_numeric_columns].join(air_numeric_interpolated)

    # Save the cleaned data to a CSV file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    air_cleaned.to_csv(output_file, index=False)

    print(f'Dataframe saved to {output_file}')

if __name__ == "__main__":
    # Define input and output paths
    input_file = '../data/raw/AirQuality_data.csv'
    output_file = '../data/processed/air_cleaned.csv'

    # Run the cleaning function
    clean_air_quality_data(input_file, output_file)