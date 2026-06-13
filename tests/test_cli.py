import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit_cli import save_macro_risk_summary, save_macro_risk_json, validate_dataset


def test_save_macro_risk_summary_creates_markdown_file(tmp_path):
    analysis = {
        "latest_year": 2024,
        "risk_score": 2,
        "overall_risk": "Moderate",
        "signals": {
            "inflation_pressure": "Normal",
            "growth_condition": "Moderate",
            "labor_market": "Tight",
            "monetary_condition": "Tight",
        },
        "summary": "This is a sample macro risk summary."
    }

    output_path = save_macro_risk_summary(analysis, tmp_path)

    assert output_path.exists()
    assert output_path.name == "macro_risk_summary.md"

    content = output_path.read_text(encoding="utf-8")

    assert "# Macro Risk Summary" in content
    assert "Overall risk: Moderate" in content
    assert "Inflation Pressure: Normal" in content
    assert "This is a sample macro risk summary." in content


def test_save_macro_risk_json_creates_json_file(tmp_path):
    analysis = {
        "latest_year": 2024,
        "risk_score": 2,
        "overall_risk": "Moderate",
        "signals": {
            "inflation_pressure": "Normal",
            "growth_condition": "Moderate",
            "labor_market": "Tight",
            "monetary_condition": "Tight",
        },
        "summary": "This is a sample macro risk summary."
    }

    output_path = save_macro_risk_json(analysis, tmp_path)

    assert output_path.exists()
    assert output_path.name == "macro_risk_summary.json"

    content = output_path.read_text(encoding="utf-8")

    assert '"overall_risk": "Moderate"' in content
    assert '"latest_year": 2024' in content


def test_validate_dataset_passes_with_required_columns():
    data = pd.DataFrame({
        "year": [2024],
        "gdp_growth": [2.0],
        "inflation_rate": [2.3],
        "unemployment_rate": [2.8],
        "interest_rate": [3.5],
    })

    assert validate_dataset(data) is True


def test_validate_dataset_raises_error_for_missing_columns():
    data = pd.DataFrame({
        "year": [2024],
        "gdp_growth": [2.0],
    })

    try:
        validate_dataset(data)
        assert False
    except ValueError as error:
        assert "Missing required columns" in str(error)


def test_validate_dataset_raises_error_for_empty_data():
    data = pd.DataFrame(columns=[
        "year",
        "gdp_growth",
        "inflation_rate",
        "unemployment_rate",
        "interest_rate",
    ])

    try:
        validate_dataset(data)
        assert False
    except ValueError as error:
        assert "Dataset is empty" in str(error)
