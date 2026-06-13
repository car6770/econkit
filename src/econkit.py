from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


REQUIRED_MACRO_COLUMNS = [
    "year",
    "gdp_growth",
    "inflation_rate",
    "unemployment_rate",
    "interest_rate",
]


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


def _validate_required_columns(data, required_columns):
    """
    Validate that a dataset contains required columns.
    """
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return True


def _is_missing(value):
    """
    Check whether a value is missing.
    """
    return value is None or value != value


def classify_inflation_pressure(inflation_rate):
    """
    Classify inflation pressure based on the latest inflation rate.
    """
    if _is_missing(inflation_rate):
        return "Unknown"

    if inflation_rate >= 4.0:
        return "High"

    if inflation_rate >= 2.5:
        return "Elevated"

    if inflation_rate < 1.0:
        return "Low"

    return "Normal"


def classify_growth_condition(gdp_growth):
    """
    Classify economic growth condition based on GDP growth.
    """
    if _is_missing(gdp_growth):
        return "Unknown"

    if gdp_growth < 0:
        return "Contraction"

    if gdp_growth < 1.5:
        return "Weak"

    if gdp_growth <= 3.0:
        return "Moderate"

    return "Strong"


def classify_labor_market(unemployment_rate):
    """
    Classify labor market condition based on unemployment rate.
    """
    if _is_missing(unemployment_rate):
        return "Unknown"

    if unemployment_rate < 3.0:
        return "Tight"

    if unemployment_rate <= 4.0:
        return "Stable"

    if unemployment_rate <= 5.0:
        return "Soft"

    return "Weak"


def classify_monetary_condition(interest_rate):
    """
    Classify monetary condition based on the interest rate.
    """
    if _is_missing(interest_rate):
        return "Unknown"

    if interest_rate >= 3.0:
        return "Tight"

    if interest_rate >= 1.5:
        return "Neutral"

    return "Accommodative"


def calculate_macro_risk_score(signals):
    """
    Calculate a simple macroeconomic risk score from classified signals.
    """
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


def classify_overall_macro_risk(score):
    """
    Classify the overall macroeconomic risk level.
    """
    if score >= 5:
        return "High"

    if score >= 3:
        return "Elevated"

    if score >= 1:
        return "Moderate"

    return "Low"


def generate_macro_risk_summary(analysis):
    """
    Generate a beginner-friendly written summary of macroeconomic conditions.
    """
    year = analysis["latest_year"]
    signals = analysis["signals"]
    overall_risk = analysis["overall_risk"]

    summary = []
    summary.append(
        f"In {year}, the overall macroeconomic risk level is classified as {overall_risk}."
    )
    summary.append(
        f"Inflation pressure is {signals['inflation_pressure'].lower()}, "
        f"while growth conditions are {signals['growth_condition'].lower()}."
    )
    summary.append(
        f"The labor market is classified as {signals['labor_market'].lower()}, "
        f"and monetary conditions are {signals['monetary_condition'].lower()}."
    )
    summary.append(
        "This classification is based on simple educational thresholds and should be "
        "interpreted as a beginner-friendly macroeconomic screening tool, not as a "
        "formal forecast."
    )

    return " ".join(summary)


def analyze_macro_risk(data):
    """
    Analyze macroeconomic risk using the latest observation in the dataset.

    Required columns:
    - year
    - gdp_growth
    - inflation_rate
    - unemployment_rate
    - interest_rate
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    latest_row = data.sort_values("year").iloc[-1]

    signals = {
        "inflation_pressure": classify_inflation_pressure(
            latest_row["inflation_rate"]
        ),
        "growth_condition": classify_growth_condition(latest_row["gdp_growth"]),
        "labor_market": classify_labor_market(latest_row["unemployment_rate"]),
        "monetary_condition": classify_monetary_condition(
            latest_row["interest_rate"]
        ),
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


def estimate_macro_baseline(data):
    """
    Estimate simple baseline macroeconomic conditions from historical data.

    This function uses recent averages as educational baseline values.
    It is not intended for professional forecasting.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    recent_data = data.sort_values("year").tail(5)

    return {
        "potential_growth": float(recent_data["gdp_growth"].mean()),
        "target_inflation": 2.0,
        "normal_unemployment": float(recent_data["unemployment_rate"].mean()),
        "neutral_interest_rate": float(recent_data["interest_rate"].mean()),
    }


def calculate_policy_rule_rate(
    inflation_rate,
    gdp_growth,
    target_inflation=2.0,
    neutral_interest_rate=2.0,
    potential_growth=2.0,
    inflation_weight=0.5,
    growth_weight=0.5,
):
    """
    Calculate a simple educational policy-rule interest rate.

    The rule raises the recommended interest rate when inflation is above target
    or when growth is above potential. It lowers the recommended rate when
    inflation is below target or growth is below potential.

    This is a simplified teaching tool inspired by monetary policy rules.
    It is not a formal central bank model.
    """
    inflation_gap = inflation_rate - target_inflation
    growth_gap = gdp_growth - potential_growth

    recommended_rate = (
        neutral_interest_rate
        + inflation_weight * inflation_gap
        + growth_weight * growth_gap
    )

    return max(0.0, recommended_rate)


def classify_policy_stance(policy_gap):
    """
    Classify monetary policy stance using the gap between actual and recommended rates.
    """
    if policy_gap >= 0.75:
        return "Tight"

    if policy_gap >= 0.25:
        return "Moderately Tight"

    if policy_gap <= -0.75:
        return "Accommodative"

    if policy_gap <= -0.25:
        return "Moderately Accommodative"

    return "Neutral"


def generate_monetary_policy_summary(analysis):
    """
    Generate a beginner-friendly written summary of monetary policy stance.
    """
    latest_year = analysis["latest_year"]
    stance = analysis["policy_stance"]
    policy_gap = analysis["policy_gap"]
    actual_rate = analysis["actual_interest_rate"]
    recommended_rate = analysis["recommended_policy_rate"]

    if policy_gap > 0:
        direction_text = "above"
    elif policy_gap < 0:
        direction_text = "below"
    else:
        direction_text = "equal to"

    summary = (
        f"In {latest_year}, monetary policy is classified as {stance}. "
        f"The actual interest rate is {actual_rate:.2f}, while the simple "
        f"policy-rule rate is {recommended_rate:.2f}. "
        f"This means the actual rate is {abs(policy_gap):.2f} percentage points "
        f"{direction_text} the educational policy-rule benchmark."
    )

    return summary


def analyze_monetary_policy_stance(
    data,
    target_inflation=2.0,
    neutral_interest_rate=None,
    potential_growth=None,
    inflation_weight=0.5,
    growth_weight=0.5,
):
    """
    Analyze whether monetary policy looks tight, neutral, or accommodative.

    Required columns:
    - year
    - gdp_growth
    - inflation_rate
    - unemployment_rate
    - interest_rate

    Returns
    -------
    dict
        Beginner-friendly monetary policy stance analysis.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

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


def generate_monetary_policy_report(data, output_path):
    """
    Generate a Markdown report for monetary policy stance analysis.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    analysis = analyze_monetary_policy_stance(data)

    lines = []
    lines.append("# Monetary Policy Stance Report")
    lines.append("")
    lines.append("This report was automatically generated with EconKit.")
    lines.append("")
    lines.append("## Policy stance")
    lines.append("")
    lines.append(f"- Latest year: {analysis['latest_year']}")
    lines.append(f"- Policy stance: {analysis['policy_stance']}")
    lines.append(f"- Actual interest rate: {analysis['actual_interest_rate']:.2f}")
    lines.append(
        f"- Recommended policy-rule rate: "
        f"{analysis['recommended_policy_rate']:.2f}"
    )
    lines.append(f"- Policy gap: {analysis['policy_gap']:.2f}")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    for name, value in analysis["inputs"].items():
        readable_name = name.replace("_", " ").title()
        lines.append(f"- {readable_name}: {value:.2f}")
    lines.append("")
    lines.append("## Economic gaps")
    lines.append("")
    for name, value in analysis["gaps"].items():
        readable_name = name.replace("_", " ").title()
        lines.append(f"- {readable_name}: {value:.2f}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(analysis["summary"])
    lines.append("")
    lines.append("## Educational note")
    lines.append("")
    lines.append(
        "This monetary policy analysis is a simplified educational tool. "
        "It should not be interpreted as an official policy recommendation."
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


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
    policy_analysis = analyze_monetary_policy_stance(data)

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
    lines.append("## Monetary policy stance")
    lines.append("")
    lines.append(f"- Policy stance: {policy_analysis['policy_stance']}")
    lines.append(
        f"- Actual interest rate: "
        f"{policy_analysis['actual_interest_rate']:.2f}"
    )
    lines.append(
        f"- Recommended policy-rule rate: "
        f"{policy_analysis['recommended_policy_rate']:.2f}"
    )
    lines.append(f"- Policy gap: {policy_analysis['policy_gap']:.2f}")
    lines.append("")
    lines.append(policy_analysis["summary"])
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

    policy_report_path = output_dir / "monetary_policy_report.md"
    generate_monetary_policy_report(data, policy_report_path)

    return report_path


def simulate_macro_scenario(
    data,
    scenario_name,
    years=5,
    demand_shock=0.0,
    supply_shock=0.0,
    policy_shock=0.0,
):
    """
    Simulate a simple macroeconomic scenario.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical macroeconomic dataset.
    scenario_name : str
        Name of the scenario.
    years : int
        Number of future years to simulate.
    demand_shock : float
        Positive values increase growth and inflation. Negative values reduce growth.
    supply_shock : float
        Positive values increase inflation and reduce growth.
    policy_shock : float
        Positive values increase the interest rate path.

    Returns
    -------
    pandas.DataFrame
        Simulated scenario dataset.
    """
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


def build_default_macro_scenarios(data, years=5):
    """
    Build a set of default macroeconomic scenarios.
    """
    return {
        "baseline": simulate_macro_scenario(
            data,
            scenario_name="baseline",
            years=years,
        ),
        "inflation_shock": simulate_macro_scenario(
            data,
            scenario_name="inflation_shock",
            years=years,
            supply_shock=2.0,
        ),
        "recession_shock": simulate_macro_scenario(
            data,
            scenario_name="recession_shock",
            years=years,
            demand_shock=-2.0,
        ),
        "tight_policy": simulate_macro_scenario(
            data,
            scenario_name="tight_policy",
            years=years,
            policy_shock=1.5,
        ),
    }


def compare_macro_scenarios(scenarios):
    """
    Compare final-year outcomes across macroeconomic scenarios.
    """
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


def generate_macro_scenario_report(scenarios, output_path):
    """
    Generate a Markdown report comparing macroeconomic scenarios.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    comparison = compare_macro_scenarios(scenarios)

    lines = []
    lines.append("# Macro Scenario Analysis Report")
    lines.append("")
    lines.append("This report was automatically generated with EconKit.")
    lines.append("")
    lines.append("## Scenario comparison")
    lines.append("")
    lines.append(comparison.to_markdown(index=False))
    lines.append("")
    lines.append("## Scenario descriptions")
    lines.append("")
    lines.append("- `baseline`: continuation of recent macroeconomic conditions")
    lines.append("- `inflation_shock`: higher inflation caused by a supply-side shock")
    lines.append("- `recession_shock`: weaker growth caused by a negative demand shock")
    lines.append("- `tight_policy`: higher interest rates caused by a monetary policy shock")
    lines.append("")
    lines.append("## Interpretation guide")
    lines.append("")
    lines.append(
        "Students can compare scenarios to understand how macroeconomic shocks may "
        "affect growth, inflation, unemployment, interest rates, and overall macro "
        "risk."
    )
    lines.append("")
    lines.append("## Educational note")
    lines.append("")
    lines.append(
        "This scenario simulator uses simple educational rules. "
        "It is not intended to be a professional forecasting model."
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def generate_macro_scenario_analysis(data_path, output_dir, years=5):
    """
    Generate scenario CSV files, comparison data, and a Markdown scenario report.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_economic_data(data_path)

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
