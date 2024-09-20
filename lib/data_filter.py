import os
import pandas as pd


def extract_dates_from_filenames(data_dir):
    dates = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            date_part = filename.split('_')[0]  # Assumes filenames are in the format 'YYYY-MM-DD_otherinfo.txt'
            dates.append(date_part)
    return dates


def filter_temperature_data(temperature_file, dates, output_file):
    try:
        # Load the original temperature data
        temp_df = pd.read_csv(temperature_file, sep="\t", header=0, parse_dates=['time'], dayfirst=True)
        print(f"Temperature data loaded successfully: {temp_df.head()}")

        # Ensure the 'time' column is in datetime format
        if not pd.api.types.is_datetime64_any_dtype(temp_df['time']):
            temp_df['time'] = pd.to_datetime(temp_df['time'], errors='coerce')
            print(f"Time column converted to datetime: {temp_df['time'].head()}")

        # Check if there are any NaT values after conversion
        if temp_df['time'].isnull().any():
            print("Warning: Some 'time' values could not be converted to datetime. Check for malformed data.")
            print(temp_df[temp_df['time'].isnull()])

        # Convert dates to pandas datetime for matching
        temp_df['date'] = temp_df['time'].dt.strftime('%Y-%m-%d')
        print(f"Processed date column: {temp_df['date'].unique()}")

        # Filter rows where the date is in the list of dates from the txt files
        filtered_df = temp_df[temp_df['date'].isin(dates)]
        print(f"Filtered data: {filtered_df.head()}")

        # Save the filtered temperature data
        filtered_df.to_csv(output_file, sep="\t", index=False)
        print(f"Filtered temperature data saved to {output_file}")

    except Exception as e:
        print(f"Error during temperature data filtering: {e}")


