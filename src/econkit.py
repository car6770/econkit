import pandas as pd


def load_economic_data(file_path):
    """
    Load an economic dataset from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded economic dataset.
    """
    return pd.read_csv(file_path)


def calculate_summary_statistics(data):
    """
    Calculate basic summary statistics for an economic dataset.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.

    Returns
    -------
    pandas.DataFrame
        Summary statistics.
    """
    return data.describe()


def calculate_average_growth(data, column):
    """
    Calculate the average value of a selected economic indicator.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.
    column : str
        Column name of the economic indicator.

    Returns
    -------
    float
        Average value of the selected column.
    """
    return data[column].mean()


def find_highest_value_year(data, column):
    """
    Find the year with the highest value for a selected economic indicator.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.
    column : str
        Column name of the economic indicator.

    Returns
    -------
    pandas.Series
        Row with the highest value.
    """
    return data.loc[data[column].idxmax()]
