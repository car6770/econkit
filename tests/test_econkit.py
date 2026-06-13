import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import (
    analyze_business_cycle,
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
    generate_economic_report,
    generate_macro_scenario_analysis,
    generate_monetary_policy_report,
    simulate_macro_scenario,
    validate_macro_dataset,
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


def test_validate_macro_dataset_passes_for_valid_data():
    assert validate_macro_dataset(make_sample_macro_data()) is True


def test_validate_macro_dataset_raises_for_missing_columns():
    data = pd.DataFrame({"year": [2024], "gdp_growth": [2.0]})
    try:
        validate_macro_dataset(data)
        assert False
    except ValueError as error:
        assert "Missing required columns" in str(error)


def test_calculate_summary_statistics():
    data = pd.DataFrame({"year": [2020, 2021, 2022], "gdp_growth": [-0.7, 4.3, 2.6]})
    summary = calculate_summary_statistics(data)
    assert "gdp_growth" in summary.columns
    assert summary.loc["count", "gdp_growth"] == 3


def test_calculate_average_growth():
    data = pd.DataFrame({"year": [2020, 2021, 2022], "gdp_growth": [-0.7, 4.3, 2.6]})
    assert round(calculate_average_growth(data, "gdp_growth"), 2) == 2.07


def test_find_highest_and_lowest_value_year():
    data = pd.DataFrame({"year": [2020, 2021, 2022], "inflation_rate": [0.5, 2.5, 5.1]})
    assert find_highest_value_year(data, "inflation_rate")["year"] == 2022
    assert find_lowest_value_year(data, "inflation_rate")["year"] == 2020


def test_calculate_correlation_matrix():
    data = pd.DataFrame({"gdp_growth": [-0.7, 4.3, 2.6], "inflation_rate": [0.5, 2.5, 5.1]})
    matrix = calculate_correlation_matrix(data, ["gdp_growth", "inflation_rate"])
    assert "gdp_growth" in matrix.columns
    assert "inflation_rate" in matrix.columns


def test_analyze_macro_risk_returns_expected_structure():
    analysis = analyze_macro_risk(make_sample_macro_data())
    assert analysis["latest_year"] == 2024
    assert analysis["overall_risk"] == "Moderate"
    assert "summary" in analysis


def test_calculate_policy_rule_rate():
    rate = calculate_policy_rule_rate(
        inflation_rate=4.0,
        gdp_growth=3.0,
        target_inflation=2.0,
        neutral_interest_rate=2.0,
        potential_growth=2.0,
    )
    assert rate == 3.5


def test_classify_policy_stance():
    assert classify_policy_stance(1.0) == "Tight"
    assert classify_policy_stance(0.5) == "Moderately Tight"
    assert classify_policy_stance(0.0) == "Neutral"
    assert classify_policy_stance(-0.5) == "Moderately Accommodative"
    assert classify_policy_stance(-1.0) == "Accommodative"


def test_analyze_monetary_policy_stance_returns_expected_values():
    analysis = analyze_monetary_policy_stance(make_sample_macro_data())
    assert analysis["latest_year"] == 2024
    assert analysis["actual_interest_rate"] == 3.5
    assert analysis["recommended_policy_rate"] == 3.57
    assert analysis["policy_gap"] == -0.07
    assert analysis["policy_stance"] == "Neutral"


def test_analyze_monetary_policy_stance_with_custom_assumptions():
    analysis = analyze_monetary_policy_stance(
        make_sample_macro_data(),
        target_inflation=2.0,
        neutral_interest_rate=2.0,
        potential_growth=2.0,
    )
    assert analysis["recommended_policy_rate"] == 2.15
    assert analysis["policy_gap"] == 1.35
    assert analysis["policy_stance"] == "Tight"


def test_analyze_business_cycle():
    analysis = analyze_business_cycle(make_sample_macro_data())
    assert analysis["latest_year"] == 2024
    assert analysis["business_cycle_phase"] == "Stable Expansion"
    assert "inflation_diagnosis" in analysis


def test_generate_monetary_policy_report_creates_markdown_file(tmp_path):
    output_path = tmp_path / "monetary_policy_report.md"
    report_path = generate_monetary_policy_report(make_sample_macro_data(), output_path)
    assert report_path.exists()
    report_text = report_path.read_text(encoding="utf-8")
    assert "# Monetary Policy Stance Report" in report_text


def test_simulate_macro_scenario_returns_future_rows():
    scenario = simulate_macro_scenario(make_sample_macro_data(), "baseline", years=3)
    assert len(scenario) == 3
    assert scenario["year"].tolist() == [2025, 2026, 2027]
    assert "interest_rate" in scenario.columns


def test_build_default_macro_scenarios_creates_expected_scenarios():
    scenarios = build_default_macro_scenarios(make_sample_macro_data(), years=2)
    assert set(scenarios.keys()) == {"baseline", "inflation_shock", "recession_shock", "tight_policy"}
    assert len(scenarios["baseline"]) == 2


def test_compare_macro_scenarios_returns_comparison_table():
    scenarios = build_default_macro_scenarios(make_sample_macro_data(), years=2)
    comparison = compare_macro_scenarios(scenarios)
    assert len(comparison) == 4
    assert "overall_risk" in comparison.columns


def test_generate_macro_scenario_analysis_creates_files(tmp_path):
    data_path = tmp_path / "sample.csv"
    make_sample_macro_data().to_csv(data_path, index=False)
    results = generate_macro_scenario_analysis(data_path, tmp_path / "outputs", years=2)
    assert results["comparison_path"].exists()
    assert results["report_path"].exists()
    assert len(results["scenario_paths"]) == 4


def test_generate_economic_report_creates_report(tmp_path):
    data_path = tmp_path / "sample.csv"
    make_sample_macro_data().to_csv(data_path, index=False)
    report_path = generate_economic_report(data_path, tmp_path / "report")
    assert report_path.exists()
