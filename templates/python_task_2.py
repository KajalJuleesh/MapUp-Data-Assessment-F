import pandas as pd
from datetime import datetime, time, timedelta

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance')
    distance_matrix = distance_matrix.fillna(0)
    for col in distance_matrix.columns:
        for row in distance_matrix.index:
            if pd.notna(distance_matrix.at[row, col]):
                distance_matrix.at[row, col] += distance_matrix.at[row, col]

    df = distance_matrix + distance_matrix.T - distance_matrix * (distance_matrix.T != 0)

    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    df = pd.melt(df.reset_index(), id_vars='index', var_name='id_end', value_name='distance')
    df['id_end'] = pd.to_numeric(df['id_end'], errors='coerce')
    df = df.dropna()
    df = df.reset_index(drop=True)
    df['id_end'] = df['id_end'].astype(str)
    df.columns = ['id_start', 'id_end', 'distance']

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_df = df[df['id_start'] == reference_id]
    if reference_df.empty:
        return pd.DataFrame(columns=['id_start', 'id_end', 'distance'])
        
    reference_avg_distance = reference_df['distance'].mean()

    lower_threshold = reference_avg_distance - (reference_avg_distance * 0.1)
    upper_threshold = reference_avg_distance + (reference_avg_distance * 0.1)
    df = df[(df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    #df = pd.read_csv(df)
    for val in range(len(df)):
        df['moto'] = 0.8*df['distance']
        df['car'] = 1.2*df['distance'] 
        df['rv'] = 1.5*df['distance'] 
        df['bus'] = 2.2*df['distance'] 
        df['truck'] = 3.6*df['distance'] 

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    time_ranges = [
        {'start': time(0, 0), 'end': time(10, 0), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start': time(10, 0), 'end': time(18, 0), 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start': time(18, 0), 'end': time(23, 59, 59), 'weekday_factor': 0.8, 'weekend_factor': 0.7},
    ]

    # Convert 'start_time' and 'end_time' to datetime.time()
    df['start_time'] = pd.to_datetime(df['id_start']).dt.time
    df['end_time'] = pd.to_datetime(df['id_end']).dt.time

    # Add columns for start_day and end_day
    df['start_day'] = pd.to_datetime(df['id_start']).dt.day_name()
    df['end_day'] = pd.to_datetime(df['end_time']).dt.day_name()

    # Calculate time-based toll rates
    for index, row in df.iterrows():
        for time_range in time_ranges:
            if (
                (row['start_time'] >= time_range['start'] and row['start_time'] <= time_range['end']) or
                (row['end_time'] >= time_range['start'] and row['end_time'] <= time_range['end'])
            ):
                discount_factor = time_range['weekday_factor'] if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else time_range['weekend_factor']
                for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
                    df.at[index, vehicle_type] *= discount_factor
                break
  return df
