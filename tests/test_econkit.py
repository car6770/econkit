import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import (
    analyze_macro_risk,
    analyze_monetary_policy_stance,
    build_default_macro_scenarios,
    calculate_average_growth,
    calculate_correlation_matrix,
    calculate_policy_rule_rate,
    calculate_summary_statistics,
    classify_policy_stance,
    compare_macro_scenarios,
    find_highest_value_year,
    find_lowest_value_year,
    generate_monetary_policy_report,
    simulate_macro_scenario,
)


def make_sample_macro_data():
    return pd.DataFrame(
        {
            "year": [2022, 2023, 2024],
            "gdp_growth": [2.6, 1.4, 2.0],
            "inflation_rate": [5.1, 3.6, 2.3],
            "unemployment_rate": [3.0, 2.7, 2.8],
            "interest_rate": [3.25, 3.50, 3.50],
        }
    )


def test_calculate_summary_statistics():
    data = pd.DataFrame(
        {
            "year": [2020, 2021, 2022],
            "gdp_growth": [-0.7, 4.3, 2.6],
        }
    )

    summary = calculate_summary_statistics(data)

    assert "gdp_growth" in summary.columns
    assert summary.loc["count", "gdp_growth"] == 3


def test_calculate_average_growth():
    data = pd.DataFrame(
        {
            "year": [2020, 2021, 2022],
            "gdp_growth": [-0.7, 4.3, 2.6],
        }
    )

    average_growth = calculate_average_growth(data, "gdp_growth")

    assert round(average_growth, 2) == 2.07


def test_find_highest_value_year():
    data = pd.DataFrame(
        {
            "year": [2020, 2021, 2022],
            "inflation_rate": [0.5, 2.5, 5.1],
        }
    )

    highest_row = find_highest_value_year(data, "inflation_rate")

    assert highest_row["year"] == 2022
    assert highest_row["inflation_rate"] == 5.1


def test_find_lowest_value_year():
    data = pd.DataFrame(
        {
            "year": [2020, 2021, 2022],
            "inflation_rate": [0.5, 2.5, 5.1],
        }
    )

    lowest_row = find_lowest_value_year(data, "inflation_rate")

    assert lowest_row["year"] == 2020
    assert lowest_row["inflation_rate"] == 0.5


def test_calculate_correlation_matrix():
    data = pd.DataFrame(
        {
            "gdp_growth": [-0.7, 4.3, 2.6],
            "inflation_rate": [0.5, 2.5, 5.1],
        }
    )

    correlation_matrix = calculate_correlation_matrix(
        data,
        ["gdp_growth", "inflation_rate"],
    )

    assert "gdp_growth" in correlation_matrix.columns
    assert "inflation_rate" in correlation_matrix.columns


def test_analyze_macro_risk_returns_expected_structure():
    data = make_sample_macro_data()

    analysis = analyze_macro_risk(data)

    assert analysis["latest_year"] == 2024
    assert "latest_values" in analysis
    assert "signals" in analysis
    assert "risk_score" in analysis
    assert "overall_risk" in analysis
    assert "summary" in analysis


def test_calculate_policy_rule_rate():
    recommended_rate = calculate_policy_rule_rate(
        inflation_rate=4.0,
        gdp_growth=3.0,
        target_inflation=2.0,
        neutral_interest_rate=2.0,
        potential_growth=2.0,
    )

    assert recommended_rate == 3.5


def test_classify_policy_stance():
    assert classify_policy_stance(1.0) == "Tight"
    assert classify_policy_stance(0.5) == "Moderately Tight"
    assert classify_policy_stance(0.0) == "Neutral"
    assert classify_policy_stance(-0.5) == "Moderately Accommodative"
    assert classify_policy_stance(-1.0) == "Accommodative"


def test_analyze_monetary_policy_stance_returns_expected_structure():
    data = make_sample_macro_data()

    analysis = analyze_monetary_policy_stance(data)

    assert analysis["latest_year"] == 2024
    assert "actual_interest_rate" in analysis
    assert "recommended_policy_rate" in analysis
    assert "policy_gap" in analysis
    assert "policy_stance" in analysis
    assert "inputs" in analysis
    assert "gaps" in analysis
    assert "summary" in analysis


def test_analyze_monetary_policy_stance_classifies_latest_policy():
    data = make_sample_macro_data()

    analysis = analyze_monetary_policy_stance(data)

    assert analysis["actual_interest_rate"] == 3.5
    assert analysis["recommended_policy_rate"] == 3.57
    assert analysis["policy_gap"] == -0.07
    assert analysis["policy_stance"] == "Neutral"


def test_analyze_monetary_policy_stance_with_custom_assumptions():
    data = make_sample_macro_data()

    analysis = analyze_monetary_policy_stance(
        data,
        target_inflation=2.0,
        neutral_interest_rate=2.0,
        potential_growth=2.0,
    )

    assert analysis["recommended_policy_rate"] == 2.15
    assert analysis["policy_gap"] == 1.35
    assert analysis["policy_stance"] == "Tight"


def test_generate_monetary_policy_report_creates_markdown_file(tmp_path):
    data = make_sample_macro_data()
    output_path = tmp_path / "monetary_policy_report.md"

    report_path = generate_monetary_policy_report(data, output_path)

    assert report_path.exists()

    report_text = report_path.read_text(encoding="utf-8")

    assert "# Monetary Policy Stance Report" in report_text
    assert "Policy stance" in report_text
    assert "Educational note" in report_text


def test_simulate_macro_scenario_returns_future_rows():
    data = make_sample_macro_data()

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
    data = make_sample_macro_data()

    scenarios = build_default_macro_scenarios(data, years=2)

    assert set(scenarios.keys()) == {
        "baseline",
        "inflation_shock",
        "recession_shock",
        "tight_policy",
    }
    assert len(scenarios["baseline"]) == 2


def test_compare_macro_scenarios_returns_comparison_table():
    data = make_sample_macro_data()

    scenarios = build_default_macro_scenarios(data, years=2)
    comparison = compare_macro_scenarios(scenarios)

    assert len(comparison) == 4
    assert "scenario" in comparison.columns
    assert "overall_risk" in comparison.columns
    assert "risk_score" in comparison.columns
