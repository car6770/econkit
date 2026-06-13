import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import calculate_average_growth, calculate_correlation_matrix, calculate_summary_statistics, find_highest_value_year, find_lowest_value_year


def test_calculate_summary_statistics():
    data = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "gdp_growth": [-0.7, 4.3, 2.6]
    })

    summary = calculate_summary_statistics(data)

    assert "gdp_growth" in summary.columns
    assert summary.loc["count", "gdp_growth"] == 3


def test_calculate_average_growth():
    data = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "gdp_growth": [-0.7, 4.3, 2.6]
    })

    average_growth = calculate_average_growth(data, "gdp_growth")

    assert round(average_growth, 2) == 2.07


def test_find_highest_value_year():
    data = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "inflation_rate": [0.5, 2.5, 5.1]
    })

    highest_row = find_highest_value_year(data, "inflation_rate")

    assert highest_row["year"] == 2022
    assert highest_row["inflation_rate"] == 5.1

def test_find_lowest_value_year():
    data = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "inflation_rate": [0.5, 2.5, 5.1]
    })

    lowest_row = find_lowest_value_year(data, "inflation_rate")

    assert lowest_row["year"] == 2020
    assert lowest_row["inflation_rate"] == 0.5


def test_calculate_correlation_matrix():
    data = pd.DataFrame({
        "gdp_growth": [-0.7, 4.3, 2.6],
        "inflation_rate": [0.5, 2.5, 5.1]
    })

    correlation_matrix = calculate_correlation_matrix(
        data,
        ["gdp_growth", "inflation_rate"]
    )

    assert "gdp_growth" in correlation_matrix.columns
    assert "inflation_rate" in correlation_matrix.columns
