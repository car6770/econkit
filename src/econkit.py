from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


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


def find_lowest_value_year(data, column):
    """
    Find the year with the lowest value for a selected economic indicator.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.
    column : str
        Column name of the economic indicator.

    Returns
    -------
    pandas.Series
        Row with the lowest value.
    """
    return data.loc[data[column].idxmin()]


def calculate_correlation_matrix(data, columns):
    """
    Calculate a correlation matrix for selected economic indicators.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.
    columns : list
        List of columns to include in the correlation matrix.

    Returns
    -------
    pandas.DataFrame
        Correlation matrix.
    """
    return data[columns].corr()


def create_line_chart(data, x_column, y_column, output_path):
    """
    Create and save a line chart for an economic indicator.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.
    x_column : str
        Column to use for the x-axis.
    y_column : str
        Column to use for the y-axis.
    output_path : str
        Path where the chart image will be saved.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(data[x_column], data[y_column], marker="o")
    plt.title(f"{y_column.replace('_', ' ').title()} Over Time")
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def generate_markdown_report(data, indicators, output_path):
    """
    Generate a beginner-friendly Markdown report for economic data.

    Parameters
    ----------
    data : pandas.DataFrame
        Economic dataset.
    indicators : list
        List of economic indicators to summarize.
    output_path : str
        Path where the Markdown report will be saved.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = calculate_summary_statistics(data[indicators])
    correlations = calculate_correlation_matrix(data, indicators)

    lines = []
    lines.append("# Economic Data Analysis Report")
    lines.append("")
    lines.append("This report was automatically generated with EconKit.")
    lines.append("")
    lines.append("## Dataset overview")
    lines.append("")
    lines.append(f"- Number of observations: {len(data)}")
    lines.append(f"- Available years: {data['year'].min()} to {data['year'].max()}")
    lines.append("")
    lines.append("## Summary statistics")
    lines.append("")
    lines.append(summary.round(2).to_markdown())
    lines.append("")
    lines.append("## Indicator highlights")
    lines.append("")

    for column in indicators:
        highest = find_highest_value_year(data, column)
        lowest = find_lowest_value_year(data, column)
        average_value = calculate_average_growth(data, column)

        readable_name = column.replace("_", " ").title()

        lines.append(f"### {readable_name}")
        lines.append("")
        lines.append(f"- Average value: {average_value:.2f}")
        lines.append(f"- Highest value: {highest[column]} in {int(highest['year'])}")
        lines.append(f"- Lowest value: {lowest[column]} in {int(lowest['year'])}")
        lines.append("")

    lines.append("## Correlation matrix")
    lines.append("")
    lines.append(correlations.round(2).to_markdown())
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "This report is intended for educational use. "
        "It helps students practice basic economic data analysis with Python."
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_economic_report(data_path, output_dir):
    """
    Generate a full economic analysis report from a CSV dataset.

    Parameters
    ----------
    data_path : str
        Path to the economic dataset.
    output_dir : str
        Directory where report files will be saved.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_economic_data(data_path)

    indicators = [
        "gdp_growth",
        "inflation_rate",
        "unemployment_rate",
        "interest_rate",
    ]

    for indicator in indicators:
        chart_path = output_dir / f"{indicator}.png"
        create_line_chart(data, "year", indicator, chart_path)

    report_path = output_dir / "economic_report.md"
    generate_markdown_report(data, indicators, report_path)

    return report_path
