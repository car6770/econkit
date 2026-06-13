import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit_cli import save_macro_risk_summary


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
