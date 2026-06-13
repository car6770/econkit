"""EconKit: beginner-friendly economics data analysis toolkit.

EconKit helps students and early researchers move from a macroeconomic CSV
file to summary statistics, charts, macro risk screening, monetary policy
stance analysis, simple scenario simulations, and Markdown reports.

The models in this file are educational rules of thumb. They are not official
forecasts, policy recommendations, or professional investment advice.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional

import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_MACRO_COLUMNS = [
    "year",
    "gdp_growth",
    "inflation_rate",
    "unemployment_rate",
    "interest_rate",
]

DEFAULT_INDICATORS = [
    "gdp_growth",
    "inflation_rate",
    "unemployment_rate",
    "interest_rate",
]


# ---------------------------------------------------------------------------
# Data loading and validation
# ---------------------------------------------------------------------------


def load_economic_data(file_path: str | Path) -> pd.DataFrame:
    """Load an economic dataset from a CSV file."""
    return pd.read_csv(file_path)


def validate_macro_dataset(data: pd.DataFrame) -> bool:
    """Validate that a dataset contains the required macroeconomic columns."""
    missing_columns = [column for column in REQUIRED_MACRO_COLUMNS if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if data.empty:
        raise ValueError("Dataset is empty.")

    return True


def _validate_required_columns(data: pd.DataFrame, required_columns: Iterable[str]) -> bool:
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return True


# ---------------------------------------------------------------------------
# Basic analysis
# ---------------------------------------------------------------------------


def calculate_summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate basic summary statistics for an economic dataset."""
    return data.describe()


def calculate_average_growth(data: pd.DataFrame, column: str) -> float:
    """Calculate the average value of a selected economic indicator."""
    return float(data[column].mean())


def find_highest_value_year(data: pd.DataFrame, column: str) -> pd.Series:
    """Find the row with the highest value for a selected indicator."""
    return data.loc[data[column].idxmax()]


def find_lowest_value_year(data: pd.DataFrame, column: str) -> pd.Series:
    """Find the row with the lowest value for a selected indicator."""
    return data.loc[data[column].idxmin()]


def calculate_correlation_matrix(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Calculate a correlation matrix for selected economic indicators."""
    return data[columns].corr()


def create_line_chart(data: pd.DataFrame, x_column: str, y_column: str, output_path: str | Path) -> Path:
    """Create and save a line chart for an economic indicator."""
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

    return output_path


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------


def _is_missing(value) -> bool:
    return value is None or value != value


def classify_inflation_pressure(inflation_rate: float) -> str:
    """Classify inflation pressure."""
    if _is_missing(inflation_rate):
        return "Unknown"
    if inflation_rate >= 4.0:
        return "High"
    if inflation_rate >= 2.5:
        return "Elevated"
    if inflation_rate < 1.0:
        return "Low"
    return "Normal"


def classify_growth_condition(gdp_growth: float) -> str:
    """Classify economic growth conditions."""
    if _is_missing(gdp_growth):
        return "Unknown"
    if gdp_growth < 0:
        return "Contraction"
    if gdp_growth < 1.5:
        return "Weak"
    if gdp_growth <= 3.0:
        return "Moderate"
    return "Strong"


def classify_labor_market(unemployment_rate: float) -> str:
    """Classify labor market conditions."""
    if _is_missing(unemployment_rate):
        return "Unknown"
    if unemployment_rate < 3.0:
        return "Tight"
    if unemployment_rate <= 4.0:
        return "Stable"
    if unemployment_rate <= 5.0:
        return "Soft"
    return "Weak"


def classify_monetary_condition(interest_rate: float) -> str:
    """Classify monetary conditions based on the interest rate."""
    if _is_missing(interest_rate):
        return "Unknown"
    if interest_rate >= 3.0:
        return "Tight"
    if interest_rate >= 1.5:
        return "Neutral"
    return "Accommodative"


# ---------------------------------------------------------------------------
# Macro risk screening
# ---------------------------------------------------------------------------


def calculate_macro_risk_score(signals: Mapping[str, str]) -> int:
    """Calculate a simple macroeconomic risk score from classified signals."""
    score = 0

    if signals["inflation_pressure"] == "High":
        score += 2
    elif signals["inflation_pressure"] == "Elevated":
        score += 1

    if signals["growth_condition"] == "Contraction":
        score += 2
    elif signals["growth_condition"] == "Weak":
        score += 1

    if signals["labor_market"] == "Weak":
        score += 2
    elif signals["labor_market"] == "Soft":
        score += 1

    if signals["monetary_condition"] == "Tight":
        score += 1

    return score


def classify_overall_macro_risk(score: int) -> str:
    """Classify the overall macroeconomic risk level."""
    if score >= 5:
        return "High"
    if score >= 3:
        return "Elevated"
    if score >= 1:
        return "Moderate"
    return "Low"


def generate_macro_risk_summary(analysis: Mapping) -> str:
    """Generate a beginner-friendly written summary of macroeconomic conditions."""
    year = analysis["latest_year"]
    signals = analysis["signals"]
    overall_risk = analysis["overall_risk"]

    return (
        f"In {year}, the overall macroeconomic risk level is classified as {overall_risk}. "
        f"Inflation pressure is {signals['inflation_pressure'].lower()}, while growth "
        f"conditions are {signals['growth_condition'].lower()}. The labor market is "
        f"classified as {signals['labor_market'].lower()}, and monetary conditions are "
        f"{signals['monetary_condition'].lower()}. This classification is based on "
        f"simple educational thresholds and should be interpreted as a screening tool, "
        f"not as a formal forecast."
    )


def analyze_macro_risk(data: pd.DataFrame) -> Dict:
    """Analyze macroeconomic risk using the latest observation in the dataset."""
    validate_macro_dataset(data)
    latest_row = data.sort_values("year").iloc[-1]

    signals = {
        "inflation_pressure": classify_inflation_pressure(float(latest_row["inflation_rate"])),
        "growth_condition": classify_growth_condition(float(latest_row["gdp_growth"])),
        "labor_market": classify_labor_market(float(latest_row["unemployment_rate"])),
        "monetary_condition": classify_monetary_condition(float(latest_row["interest_rate"])),
    }

    risk_score = calculate_macro_risk_score(signals)
    overall_risk = classify_overall_macro_risk(risk_score)

    analysis = {
        "latest_year": int(latest_row["year"]),
        "latest_values": {
            "gdp_growth": float(latest_row["gdp_growth"]),
            "inflation_rate": float(latest_row["inflation_rate"]),
            "unemployment_rate": float(latest_row["unemployment_rate"]),
            "interest_rate": float(latest_row["interest_rate"]),
        },
        "signals": signals,
        "risk_score": risk_score,
        "overall_risk": overall_risk,
    }
    analysis["summary"] = generate_macro_risk_summary(analysis)
    return analysis


# ---------------------------------------------------------------------------
# Monetary policy stance analysis
# ---------------------------------------------------------------------------


def estimate_macro_baseline(data: pd.DataFrame) -> Dict[str, float]:
    """Estimate baseline macroeconomic conditions from recent historical averages."""
    validate_macro_dataset(data)
    recent_data = data.sort_values("year").tail(5)

    return {
        "potential_growth": float(recent_data["gdp_growth"].mean()),
        "target_inflation": 2.0,
        "normal_unemployment": float(recent_data["unemployment_rate"].mean()),
        "neutral_interest_rate": float(recent_data["interest_rate"].mean()),
    }


def calculate_policy_rule_rate(
    inflation_rate: float,
    gdp_growth: float,
    target_inflation: float = 2.0,
    neutral_interest_rate: float = 2.0,
    potential_growth: float = 2.0,
    inflation_weight: float = 0.5,
    growth_weight: float = 0.5,
) -> float:
    """Calculate a simplified educational policy-rule interest rate."""
    inflation_gap = inflation_rate - target_inflation
    growth_gap = gdp_growth - potential_growth

    recommended_rate = (
        neutral_interest_rate
        + inflation_weight * inflation_gap
        + growth_weight * growth_gap
    )

    return max(0.0, float(recommended_rate))


def classify_policy_stance(policy_gap: float) -> str:
    """Classify monetary policy stance using actual minus benchmark rate."""
    if policy_gap >= 0.75:
        return "Tight"
    if policy_gap >= 0.25:
        return "Moderately Tight"
    if policy_gap <= -0.75:
        return "Accommodative"
    if policy_gap <= -0.25:
        return "Moderately Accommodative"
    return "Neutral"


def generate_monetary_policy_summary(analysis: Mapping) -> str:
    """Generate a beginner-friendly summary of monetary policy stance."""
    policy_gap = analysis["policy_gap"]
    if policy_gap > 0:
        direction_text = "above"
    elif policy_gap < 0:
        direction_text = "below"
    else:
        direction_text = "equal to"

    return (
        f"In {analysis['latest_year']}, monetary policy is classified as "
        f"{analysis['policy_stance']}. The actual interest rate is "
        f"{analysis['actual_interest_rate']:.2f}, while the simple policy-rule rate "
        f"is {analysis['recommended_policy_rate']:.2f}. This means the actual rate "
        f"is {abs(policy_gap):.2f} percentage points {direction_text} the educational "
        f"policy-rule benchmark."
    )


def analyze_monetary_policy_stance(
    data: pd.DataFrame,
    target_inflation: float = 2.0,
    neutral_interest_rate: Optional[float] = None,
    potential_growth: Optional[float] = None,
    inflation_weight: float = 0.5,
    growth_weight: float = 0.5,
) -> Dict:
    """Analyze whether policy looks tight, neutral, or accommodative."""
    validate_macro_dataset(data)
    baseline = estimate_macro_baseline(data)

    if neutral_interest_rate is None:
        neutral_interest_rate = baseline["neutral_interest_rate"]
    if potential_growth is None:
        potential_growth = baseline["potential_growth"]

    latest_row = data.sort_values("year").iloc[-1]
    actual_interest_rate = float(latest_row["interest_rate"])
    inflation_rate = float(latest_row["inflation_rate"])
    gdp_growth = float(latest_row["gdp_growth"])

    recommended_policy_rate = calculate_policy_rule_rate(
        inflation_rate=inflation_rate,
        gdp_growth=gdp_growth,
        target_inflation=target_inflation,
        neutral_interest_rate=neutral_interest_rate,
        potential_growth=potential_growth,
        inflation_weight=inflation_weight,
        growth_weight=growth_weight,
    )

    policy_gap = actual_interest_rate - recommended_policy_rate
    policy_stance = classify_policy_stance(policy_gap)

    analysis = {
        "latest_year": int(latest_row["year"]),
        "actual_interest_rate": round(actual_interest_rate, 2),
        "recommended_policy_rate": round(recommended_policy_rate, 2),
        "policy_gap": round(policy_gap, 2),
        "policy_stance": policy_stance,
        "inputs": {
            "inflation_rate": round(inflation_rate, 2),
            "gdp_growth": round(gdp_growth, 2),
            "target_inflation": round(float(target_inflation), 2),
            "neutral_interest_rate": round(float(neutral_interest_rate), 2),
            "potential_growth": round(float(potential_growth), 2),
            "inflation_weight": round(float(inflation_weight), 2),
            "growth_weight": round(float(growth_weight), 2),
        },
        "gaps": {
            "inflation_gap": round(inflation_rate - target_inflation, 2),
            "growth_gap": round(gdp_growth - potential_growth, 2),
        },
    }
    analysis["summary"] = generate_monetary_policy_summary(analysis)
    return analysis


# ---------------------------------------------------------------------------
# Economic cycle and inflation diagnosis
# ---------------------------------------------------------------------------


def classify_business_cycle(gdp_growth: float, unemployment_rate: float, inflation_rate: float) -> str:
    """Classify a simple business-cycle phase."""
    if gdp_growth < 0:
        return "Recession"
    if gdp_growth < 1.5 and unemployment_rate >= 4.0:
        return "Weak Recovery"
    if gdp_growth > 3.0 and inflation_rate >= 3.0:
        return "Overheating"
    if 1.5 <= gdp_growth <= 3.0:
        return "Stable Expansion"
    return "Expansion"


def diagnose_inflation_source(gdp_growth: float, inflation_rate: float, unemployment_rate: float) -> str:
    """Provide a simple educational diagnosis of inflation pressure."""
    if inflation_rate < 2.0:
        return "Low inflation environment"
    if inflation_rate >= 3.0 and gdp_growth > 2.5 and unemployment_rate < 4.0:
        return "Demand-side inflation pressure"
    if inflation_rate >= 3.0 and gdp_growth < 1.5:
        return "Supply-side or stagflation-style pressure"
    if inflation_rate >= 3.0:
        return "Broad inflation pressure"
    return "Contained inflation pressure"


def analyze_business_cycle(data: pd.DataFrame) -> Dict:
    """Analyze the latest business-cycle phase using simple educational rules."""
    validate_macro_dataset(data)
    latest_row = data.sort_values("year").iloc[-1]

    gdp_growth = float(latest_row["gdp_growth"])
    inflation_rate = float(latest_row["inflation_rate"])
    unemployment_rate = float(latest_row["unemployment_rate"])

    phase = classify_business_cycle(gdp_growth, unemployment_rate, inflation_rate)
    inflation_source = diagnose_inflation_source(gdp_growth, inflation_rate, unemployment_rate)

    summary = (
        f"In {int(latest_row['year'])}, the economy is classified as {phase}. "
        f"The inflation diagnosis is: {inflation_source}. This is a simple educational "
        f"classification based on GDP growth, inflation, and unemployment."
    )

    return {
        "latest_year": int(latest_row["year"]),
        "business_cycle_phase": phase,
        "inflation_diagnosis": inflation_source,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Scenario simulation
# ---------------------------------------------------------------------------


def simulate_macro_scenario(
    data: pd.DataFrame,
    scenario_name: str,
    years: int = 5,
    demand_shock: float = 0.0,
    supply_shock: float = 0.0,
    policy_shock: float = 0.0,
) -> pd.DataFrame:
    """Simulate a simple macroeconomic scenario."""
    validate_macro_dataset(data)
    baseline = estimate_macro_baseline(data)
    latest_row = data.sort_values("year").iloc[-1]

    previous_gdp_growth = float(latest_row["gdp_growth"])
    previous_inflation = float(latest_row["inflation_rate"])
    previous_unemployment = float(latest_row["unemployment_rate"])
    latest_year = int(latest_row["year"])

    potential_growth = baseline["potential_growth"]
    target_inflation = baseline["target_inflation"]
    normal_unemployment = baseline["normal_unemployment"]
    neutral_interest_rate = baseline["neutral_interest_rate"]

    results = []

    for step in range(1, years + 1):
        year = latest_year + step
        shock_decay = 0.65 ** (step - 1)

        current_demand_shock = demand_shock * shock_decay
        current_supply_shock = supply_shock * shock_decay
        current_policy_shock = policy_shock * shock_decay

        interest_rate = (
            neutral_interest_rate
            + 0.45 * (previous_inflation - target_inflation)
            + 0.20 * (previous_gdp_growth - potential_growth)
            + current_policy_shock
        )
        interest_rate = max(0.0, interest_rate)

        gdp_growth = (
            0.55 * previous_gdp_growth
            + 0.45 * potential_growth
            + current_demand_shock
            - 0.20 * max(interest_rate - neutral_interest_rate, 0)
            - 0.25 * current_supply_shock
        )

        inflation_rate = (
            0.60 * previous_inflation
            + 0.40 * target_inflation
            + 0.30 * max(gdp_growth - potential_growth, 0)
            + 0.55 * current_supply_shock
            - 0.15 * max(interest_rate - neutral_interest_rate, 0)
        )

        unemployment_rate = (
            0.70 * previous_unemployment
            + 0.30 * normal_unemployment
            - 0.35 * (gdp_growth - potential_growth)
        )
        unemployment_rate = max(0.0, unemployment_rate)

        results.append(
            {
                "scenario": scenario_name,
                "year": year,
                "gdp_growth": round(gdp_growth, 2),
                "inflation_rate": round(inflation_rate, 2),
                "unemployment_rate": round(unemployment_rate, 2),
                "interest_rate": round(interest_rate, 2),
            }
        )

        previous_gdp_growth = gdp_growth
        previous_inflation = inflation_rate
        previous_unemployment = unemployment_rate

    return pd.DataFrame(results)


def build_default_macro_scenarios(data: pd.DataFrame, years: int = 5) -> Dict[str, pd.DataFrame]:
    """Build a default scenario set."""
    return {
        "baseline": simulate_macro_scenario(data, "baseline", years=years),
        "inflation_shock": simulate_macro_scenario(data, "inflation_shock", years=years, supply_shock=2.0),
        "recession_shock": simulate_macro_scenario(data, "recession_shock", years=years, demand_shock=-2.0),
        "tight_policy": simulate_macro_scenario(data, "tight_policy", years=years, policy_shock=1.5),
    }


def compare_macro_scenarios(scenarios: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    """Compare final-year outcomes across macroeconomic scenarios."""
    rows = []

    for scenario_name, scenario_data in scenarios.items():
        final_row = scenario_data.sort_values("year").iloc[-1]
        risk_analysis = analyze_macro_risk(scenario_data)

        rows.append(
            {
                "scenario": scenario_name,
                "final_year": int(final_row["year"]),
                "final_gdp_growth": float(final_row["gdp_growth"]),
                "final_inflation_rate": float(final_row["inflation_rate"]),
                "final_unemployment_rate": float(final_row["unemployment_rate"]),
                "final_interest_rate": float(final_row["interest_rate"]),
                "overall_risk": risk_analysis["overall_risk"],
                "risk_score": risk_analysis["risk_score"],
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Reports and export helpers
# ---------------------------------------------------------------------------


def save_json(data: Mapping, output_path: str | Path) -> Path:
    """Save a dictionary as a JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return output_path


def _markdown_table(data: pd.DataFrame) -> str:
    """Return a Markdown table without requiring optional dependencies."""
    try:
        return data.to_markdown(index=False)
    except Exception:
        return data.to_string(index=False)


def generate_monetary_policy_report(data: pd.DataFrame, output_path: str | Path) -> Path:
    """Generate a Markdown monetary policy stance report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    analysis = analyze_monetary_policy_stance(data)

    lines = [
        "# Monetary Policy Stance Report",
        "",
        "This report was automatically generated with EconKit.",
        "",
        "## Policy stance",
        "",
        f"- Latest year: {analysis['latest_year']}",
        f"- Policy stance: {analysis['policy_stance']}",
        f"- Actual interest rate: {analysis['actual_interest_rate']:.2f}",
        f"- Recommended policy-rule rate: {analysis['recommended_policy_rate']:.2f}",
        f"- Policy gap: {analysis['policy_gap']:.2f}",
        "",
        "## Summary",
        "",
        analysis["summary"],
        "",
        "## Educational note",
        "",
        "This analysis is a simplified educational tool, not an official policy recommendation.",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def generate_macro_scenario_report(scenarios: Mapping[str, pd.DataFrame], output_path: str | Path) -> Path:
    """Generate a Markdown scenario comparison report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison = compare_macro_scenarios(scenarios)

    lines = [
        "# Macro Scenario Analysis Report",
        "",
        "This report was automatically generated with EconKit.",
        "",
        "## Scenario comparison",
        "",
        _markdown_table(comparison),
        "",
        "## Scenario descriptions",
        "",
        "- `baseline`: continuation of recent macroeconomic conditions",
        "- `inflation_shock`: higher inflation caused by a supply-side shock",
        "- `recession_shock`: weaker growth caused by a negative demand shock",
        "- `tight_policy`: higher interest rates caused by a monetary policy shock",
        "",
        "## Educational note",
        "",
        "This scenario simulator uses simple educational rules and is not a professional forecast.",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def generate_markdown_report(data: pd.DataFrame, indicators: list[str], output_path: str | Path) -> Path:
    """Generate a beginner-friendly Markdown report for economic data."""
    validate_macro_dataset(data)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = calculate_summary_statistics(data[indicators]).round(2)
    correlations = calculate_correlation_matrix(data, indicators).round(2)
    risk_analysis = analyze_macro_risk(data)
    policy_analysis = analyze_monetary_policy_stance(data)
    cycle_analysis = analyze_business_cycle(data)

    lines = [
        "# Economic Data Analysis Report",
        "",
        "This report was automatically generated with EconKit.",
        "",
        "## Dataset overview",
        "",
        f"- Number of observations: {len(data)}",
        f"- Available years: {int(data['year'].min())} to {int(data['year'].max())}",
        "",
        "## Summary statistics",
        "",
        summary.to_markdown(),
        "",
        "## Indicator highlights",
        "",
    ]

    for column in indicators:
        highest = find_highest_value_year(data, column)
        lowest = find_lowest_value_year(data, column)
        average_value = calculate_average_growth(data, column)
        readable_name = column.replace("_", " ").title()

        lines.extend(
            [
                f"### {readable_name}",
                "",
                f"- Average value: {average_value:.2f}",
                f"- Highest value: {highest[column]} in {int(highest['year'])}",
                f"- Lowest value: {lowest[column]} in {int(lowest['year'])}",
                "",
            ]
        )

    lines.extend(
        [
            "## Correlation matrix",
            "",
            correlations.to_markdown(),
            "",
            "## Macro risk",
            "",
            f"- Overall macro risk: {risk_analysis['overall_risk']}",
            f"- Risk score: {risk_analysis['risk_score']}",
            "",
            risk_analysis["summary"],
            "",
            "## Monetary policy stance",
            "",
            f"- Policy stance: {policy_analysis['policy_stance']}",
            f"- Actual interest rate: {policy_analysis['actual_interest_rate']:.2f}",
            f"- Recommended policy-rule rate: {policy_analysis['recommended_policy_rate']:.2f}",
            f"- Policy gap: {policy_analysis['policy_gap']:.2f}",
            "",
            policy_analysis["summary"],
            "",
            "## Business cycle diagnosis",
            "",
            f"- Business-cycle phase: {cycle_analysis['business_cycle_phase']}",
            f"- Inflation diagnosis: {cycle_analysis['inflation_diagnosis']}",
            "",
            cycle_analysis["summary"],
            "",
            "## Notes",
            "",
            "This report is intended for educational use and should not be interpreted as a formal forecast.",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def generate_economic_report(data_path: str | Path, output_dir: str | Path) -> Path:
    """Generate a full economic report and charts from a CSV dataset."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = load_economic_data(data_path)
    validate_macro_dataset(data)

    for indicator in DEFAULT_INDICATORS:
        create_line_chart(data, "year", indicator, output_dir / f"{indicator}.png")

    report_path = output_dir / "economic_report.md"
    generate_markdown_report(data, DEFAULT_INDICATORS, report_path)
    generate_monetary_policy_report(data, output_dir / "monetary_policy_report.md")

    return report_path


def generate_macro_scenario_analysis(data_path: str | Path, output_dir: str | Path, years: int = 5) -> Dict:
    """Generate scenario CSV files, comparison data, and a Markdown scenario report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = load_economic_data(data_path)
    validate_macro_dataset(data)

    scenarios = build_default_macro_scenarios(data, years=years)
    scenario_paths = {}

    for scenario_name, scenario_data in scenarios.items():
        scenario_path = output_dir / f"{scenario_name}_scenario.csv"
        scenario_data.to_csv(scenario_path, index=False)
        scenario_paths[scenario_name] = scenario_path

    comparison = compare_macro_scenarios(scenarios)
    comparison_path = output_dir / "scenario_comparison.csv"
    comparison.to_csv(comparison_path, index=False)

    report_path = output_dir / "macro_scenario_report.md"
    generate_macro_scenario_report(scenarios, report_path)

    return {
        "scenario_paths": scenario_paths,
        "comparison_path": comparison_path,
        "report_path": report_path,
    }
