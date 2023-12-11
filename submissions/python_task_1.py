import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    dataset = df.copy()
    car_matrix = dataset.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal to 0
    car_matrix.values[[range(len(car_matrix))]*2] = 0

    return car_matrix


import numpy as np
def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts



def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
   
    data = pd.read_csv(df)
    mean_column_bus = data['bus'].mean()
    index_list = []
    for val in data.bus:
        if val > 2*mean_column_bus:
            index_list.append(val)
            
    index_list.sort()
    return index_list



def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    data = pd.read_csv(df)
    avg_column_truck = data['bus'].mean()
    index_list = []
    for val in data.route:
        if val > 7*avg_column_truck:
            index_list.append(val)
            
    index_list.sort()
    return index_list



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.copy()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 20:
                modified_matrix[i][j] = matrix[i][j] * 0.75
            else:
                modified_matrix[i][j] = matrix[i][j] * 1.25

    return modified_matrix

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = df['end_timestamp'] - df['start_timestamp']
    completeness_check = df.groupby(['id', 'id_2'])['duration'].apply(
        lambda x: (x.max() - x.min()) >= pd.Timedelta(days=7, hours=23, minutes=59, seconds=59)
    )

    return completeness_check
    return pd.Series()
