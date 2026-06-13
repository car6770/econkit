import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import (
    analyze_business_cycle,
    analyze_inflation_pressure,
    analyze_macro_risk,
    analyze_monetary_policy_stance,
    analyze_policy_mix,
    build_default_macro_scenarios,
    calculate_average_growth,
    calculate_correlation_matrix,
    calculate_policy_rule_rate,
    calculate_summary_statistics,
    clean_macro_dataset,
    compare_macro_scenarios,
    find_highest_value_year,
    find_lowest_value_year,
    forecast_moving_average,
    generate_macro_scenario_analysis,
    generate_monetary_policy_report,
    list_available_features,
    parse_formula,
    profile_dataset,
    run_ols,
    run_ols_formula,
    simulate_macro_scenario,
    validate_macro_dataset,
)


def make_sample_macro_data():
    return pd.DataFrame(
        {
            "year": [2020, 2021, 2022, 2023, 2024],
            "gdp_growth": [-0.7, 4.3, 2.6, 1.4, 2.0],
            "inflation_rate": [0.5, 2.5, 5.1, 3.6, 2.3],
            "unemployment_rate": [4.0, 3.7, 3.0, 2.7, 2.8],
            "interest_rate": [0.5, 1.0, 3.25, 3.50, 3.50],
        }
    )


def test_clean_and_validate_macro_dataset():
    raw = pd.DataFrame(
        {
            "Year": ["2022", "2023", "2024"],
            "GDP Growth": ["2.6", "1.4", "2.0"],
            "Inflation Rate": ["5.1", "3.6", "2.3"],
            "Unemployment Rate": ["3.0", "2.7", "2.8"],
            "Interest Rate": ["3.25", "3.50", "3.50"],
        }
    )

    data = clean_macro_dataset(raw)

    assert "gdp_growth" in data.columns
    assert data["year"].tolist() == [2022, 2023, 2024]
    assert validate_macro_dataset(data) is True


def test_profile_dataset_returns_useful_metadata():
    data = make_sample_macro_data()

    profile = profile_dataset(data)

    assert profile.rows == 5
    assert profile.columns == 5
    assert "gdp_growth" in profile.numeric_columns
    assert profile.year_min == 2020
    assert profile.year_max == 2024


def test_calculate_summary_statistics():
    data = make_sample_macro_data()

    summary = calculate_summary_statistics(data)

    assert "gdp_growth" in summary.columns
    assert summary.loc["count", "gdp_growth"] == 5


def test_calculate_average_growth():
    data = make_sample_macro_data()

    average_growth = calculate_average_growth(data, "gdp_growth")

    assert round(average_growth, 2) == 1.92


def test_find_highest_value_year():
    data = make_sample_macro_data()

    highest_row = find_highest_value_year(data, "inflation_rate")

    assert highest_row["year"] == 2022
    assert highest_row["inflation_rate"] == 5.1


def test_find_lowest_value_year():
    data = make_sample_macro_data()

    lowest_row = find_lowest_value_year(data, "inflation_rate")

    assert lowest_row["year"] == 2020
    assert lowest_row["inflation_rate"] == 0.5


def test_calculate_correlation_matrix():
    data = make_sample_macro_data()

    correlation_matrix = calculate_correlation_matrix(
        data,
        ["gdp_growth", "inflation_rate"],
    )

    assert correlation_matrix.shape == (2, 2)
    assert "gdp_growth" in correlation_matrix.columns


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


def test_generate_monetary_policy_report_creates_markdown_file(tmp_path):
    data = make_sample_macro_data()
    output_path = tmp_path / "monetary_policy_report.md"

    report_path = generate_monetary_policy_report(data, output_path)

    assert report_path.exists()
    report_text = report_path.read_text(encoding="utf-8")
    assert "# Monetary Policy Stance Report" in report_text
    assert "Policy stance" in report_text


def test_analyze_business_cycle_is_backward_compatible():
    data = make_sample_macro_data()

    analysis = analyze_business_cycle(data)
    phase = analysis.get("business_cycle_phase", analysis.get("phase"))

    assert analysis["latest_year"] == 2024
    assert isinstance(phase, str)
    assert len(phase) > 0
    assert "summary" in analysis


def test_analyze_inflation_pressure_returns_expected_structure():
    data = make_sample_macro_data()

    analysis = analyze_inflation_pressure(data)

    assert analysis["latest_year"] == 2024
    assert "inflation_rate" in analysis
    assert "inflation_gap" in analysis
    assert "pressure" in analysis
    assert "summary" in analysis


def test_analyze_policy_mix_combines_diagnostics():
    data = make_sample_macro_data()

    analysis = analyze_policy_mix(data)

    assert "regime" in analysis
    assert "score" in analysis
    assert "macro_risk" in analysis
    assert "monetary_policy" in analysis
    assert "business_cycle" in analysis
    assert "inflation_pressure" in analysis
    assert "summary" in analysis


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


def test_generate_macro_scenario_analysis_creates_files(tmp_path):
    data = make_sample_macro_data()
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


def test_forecast_moving_average_returns_future_forecasts():
    data = make_sample_macro_data()

    forecast = forecast_moving_average(data, "gdp_growth", periods=3, window=2)

    assert len(forecast) == 3
    assert forecast["year"].tolist() == [2025, 2026, 2027]
    assert "forecast" in forecast.columns


def test_parse_formula():
    y_column, x_columns = parse_formula(
        "inflation_rate ~ gdp_growth + unemployment_rate"
    )

    assert y_column == "inflation_rate"
    assert x_columns == ["gdp_growth", "unemployment_rate"]


def test_run_ols_returns_regression_result():
    data = make_sample_macro_data()

    result = run_ols(
        data,
        y_column="inflation_rate",
        x_columns=["gdp_growth", "unemployment_rate"],
    )

    assert result.dependent_variable == "inflation_rate"
    assert "const" in result.coefficients
    assert "gdp_growth" in result.coefficients
    assert result.nobs == 5


def test_run_ols_formula_returns_regression_result():
    data = make_sample_macro_data()

    result = run_ols_formula(
        data,
        "inflation_rate ~ gdp_growth + unemployment_rate",
    )

    assert result.dependent_variable == "inflation_rate"
    assert result.independent_variables == ["gdp_growth", "unemployment_rate"]


def test_list_available_features_contains_professional_features():
    features = list_available_features()

    assert "macro risk analysis" in features
    assert "monetary policy stance analysis" in features
    assert "OLS regression" in features
    assert "stress-test scenarios" in features
