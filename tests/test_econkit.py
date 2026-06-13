import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import (
    analyze_macro_risk,
    build_default_macro_scenarios,
    calculate_average_growth,
    calculate_correlation_matrix,
    calculate_summary_statistics,
    compare_macro_scenarios,
    find_highest_value_year,
    find_lowest_value_year,
    generate_macro_scenario_analysis,
    simulate_macro_scenario,
)


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


def test_analyze_macro_risk_returns_expected_structure():
    data = pd.DataFrame({
        "year": [2022, 2023, 2024],
        "gdp_growth": [2.6, 1.4, 2.0],
        "inflation_rate": [5.1, 3.6, 2.3],
        "unemployment_rate": [3.0, 2.7, 2.8],
        "interest_rate": [3.25, 3.50, 3.50]
    })

    analysis = analyze_macro_risk(data)

    assert analysis["latest_year"] == 2024
    assert "latest_values" in analysis
    assert "signals" in analysis
    assert "risk_score" in analysis
    assert "overall_risk" in analysis
    assert "summary" in analysis


def test_analyze_macro_risk_classifies_latest_values():
    data = pd.DataFrame({
        "year": [2022, 2023, 2024],
        "gdp_growth": [2.6, 1.4, 2.0],
        "inflation_rate": [5.1, 3.6, 2.3],
        "unemployment_rate": [3.0, 2.7, 2.8],
        "interest_rate": [3.25, 3.50, 3.50]
    })

    analysis = analyze_macro_risk(data)

    assert analysis["signals"]["inflation_pressure"] == "Normal"
    assert analysis["signals"]["growth_condition"] == "Moderate"
    assert analysis["signals"]["labor_market"] == "Tight"
    assert analysis["signals"]["monetary_condition"] == "Tight"
    assert analysis["overall_risk"] == "Moderate"


def test_analyze_macro_risk_raises_error_for_missing_columns():
    data = pd.DataFrame({
        "year": [2024],
        "gdp_growth": [2.0],
        "inflation_rate": [2.3]
    })

    try:
        analyze_macro_risk(data)
        assert False
    except ValueError as error:
        assert "Missing required columns" in str(error)


def test_simulate_macro_scenario_returns_future_rows():
    data = pd.DataFrame({
        "year": [2022, 2023, 2024],
        "gdp_growth": [2.6, 1.4, 2.0],
        "inflation_rate": [5.1, 3.6, 2.3],
        "unemployment_rate": [3.0, 2.7, 2.8],
        "interest_rate": [3.25, 3.50, 3.50]
    })

    scenario = simulate_macro_scenario(
        data,
        scenario_name="baseline",
        years=3,
    )

    assert len(scenario) == 3
    assert scenario["year"].tolist() == [2025, 2026, 2027]
    assert "gdp_growth" in scenario.columns
    assert "inflation_rate" in scenario.columns
    assert "unemployment_rate" in scenario.columns
    assert "interest_rate" in scenario.columns


def test_build_default_macro_scenarios_creates_expected_scenarios():
    data = pd.DataFrame({
        "year": [2022, 2023, 2024],
        "gdp_growth": [2.6, 1.4, 2.0],
        "inflation_rate": [5.1, 3.6, 2.3],
        "unemployment_rate": [3.0, 2.7, 2.8],
        "interest_rate": [3.25, 3.50, 3.50]
    })

    scenarios = build_default_macro_scenarios(data, years=2)

    assert set(scenarios.keys()) == {
        "baseline",
        "inflation_shock",
        "recession_shock",
        "tight_policy",
    }
    assert len(scenarios["baseline"]) == 2


def test_compare_macro_scenarios_returns_comparison_table():
    data = pd.DataFrame({
        "year": [2022, 2023, 2024],
        "gdp_growth": [2.6, 1.4, 2.0],
        "inflation_rate": [5.1, 3.6, 2.3],
        "unemployment_rate": [3.0, 2.7, 2.8],
        "interest_rate": [3.25, 3.50, 3.50]
    })

    scenarios = build_default_macro_scenarios(data, years=2)
    comparison = compare_macro_scenarios(scenarios)

    assert len(comparison) == 4
    assert "scenario" in comparison.columns
    assert "overall_risk" in comparison.columns
    assert "risk_score" in comparison.columns


def test_generate_macro_scenario_analysis_creates_files(tmp_path):
    data = pd.DataFrame({
        "year": [2022, 2023, 2024],
        "gdp_growth": [2.6, 1.4, 2.0],
        "inflation_rate": [5.1, 3.6, 2.3],
        "unemployment_rate": [3.0, 2.7, 2.8],
        "interest_rate": [3.25, 3.50, 3.50]
    })

    data_path = tmp_path / "sample.csv"
    data.to_csv(data_path, index=False)

    results = generate_macro_scenario_analysis(
        data_path=data_path,
        output_dir=tmp_path / "outputs",
        years=2,
    )

    assert results["comparison_path"].exists()
    assert results["report_path"].exists()
    assert len(results["scenario_paths"]) == 4
