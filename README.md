# EconKit

[![Run Tests](https://github.com/car6770/econkit/actions/workflows/tests.yml/badge.svg)](https://github.com/car6770/econkit/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success)](https://github.com/car6770/econkit)

**EconKit** is a Python toolkit for economics data analysis, macroeconomic diagnostics, scenario simulation, forecasting, lightweight econometrics, and automated report generation.

It is designed for students, early researchers, policy-minded analysts, and anyone who wants to move from raw macroeconomic data to clear, reproducible economic interpretation.

EconKit focuses on three principles:

1. **Transparency** — every calculation is simple, readable, and auditable.
2. **Education** — outputs are designed to help users understand economic reasoning.
3. **Practicality** — reports, charts, forecasts, scenarios, and regression outputs can be generated quickly from a CSV file.

---

## What EconKit Can Do

EconKit can help users:

- Load and clean economic datasets
- Validate required macroeconomic columns
- Create data-quality reports
- Calculate summary statistics
- Build correlation matrices
- Generate line charts, multi-line charts, and scatter charts
- Diagnose macroeconomic risk
- Analyze monetary policy stance
- Estimate real interest rates
- Compare actual policy rates with a simple policy-rule benchmark
- Diagnose business-cycle conditions
- Analyze inflation pressure and momentum
- Evaluate a macroeconomic policy mix
- Simulate baseline and stress-test macro scenarios
- Generate AR(1) and moving-average forecasts
- Run lightweight OLS regression
- Use a simple regression formula interface
- Generate Markdown reports
- Export JSON diagnostics
- Create a full analysis package from one dataset

---

## Why EconKit Exists

Many economics students and early researchers want to analyze real-world economic data but struggle with three things:

1. Organizing data into a clean structure
2. Writing Python code for repeated analysis tasks
3. Turning numbers into readable economic interpretation

EconKit helps bridge that gap.

It is not just a plotting script. It is a small applied economics workflow engine.

A user can start with a dataset such as:

```text
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
2020,-0.7,0.5,4.0,0.5
2021,4.3,2.5,3.7,1.0
2022,2.6,5.1,3.0,3.25
2023,1.4,3.6,2.7,3.50
2024,2.0,2.3,2.8,3.50
```

and produce:

- Charts
- Summary tables
- Macro risk diagnostics
- Monetary policy analysis
- Business-cycle interpretation
- Inflation analysis
- Forecasts
- Scenario simulations
- Regression output
- Markdown reports

---

## Required Dataset Format

For the main macroeconomic workflow, EconKit expects a dataset with the following columns:

| Column | Meaning |
|---|---|
| `year` | Observation year |
| `gdp_growth` | GDP growth rate |
| `inflation_rate` | Inflation rate |
| `unemployment_rate` | Unemployment rate |
| `interest_rate` | Policy or short-term interest rate |

Example:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
2020,-0.7,0.5,4.0,0.5
2021,4.3,2.5,3.7,1.0
2022,2.6,5.1,3.0,3.25
2023,1.4,3.6,2.7,3.50
2024,2.0,2.3,2.8,3.50
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/car6770/econkit.git
cd econkit
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If using editable package mode:

```bash
pip install -e .
```

For development and testing:

```bash
pip install -e ".[dev]"
pytest
```

---

## Quick Start

Run the full EconKit workflow:

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

This creates a complete analysis output folder including:

- Economic report
- Macro risk analysis
- Monetary policy analysis
- Business-cycle diagnosis
- Inflation pressure diagnosis
- Policy-mix diagnosis
- Scenario simulations
- Forecast table
- Charts
- JSON outputs

---

## Documentation

EconKit includes detailed documentation for users, students, and contributors.

| Document | Purpose |
|---|---|
| [Documentation Hub](docs/README.md) | Start here for the full documentation map |
| [API Reference](docs/api.md) | Python function reference |
| [CLI Guide](docs/cli.md) | Command-line usage guide |
| [Examples Guide](docs/examples.md) | Explanation of all example scripts |
| [Methodology](docs/methodology.md) | How EconKit's analysis logic works |
| [Architecture](docs/architecture.md) | Project structure and design |
| [Troubleshooting](docs/troubleshooting.md) | Common errors and fixes |
| [Glossary](docs/glossary.md) | Economics and data-analysis terms |
| [FAQ](docs/faq.md) | Common questions |
| [Project Vision](docs/project_vision.md) | Long-term purpose and direction |
| [Release Checklist](docs/release_checklist.md) | Release preparation checklist |

Recommended starting points:

- New users: [Examples Guide](docs/examples.md)
- Python users: [API Reference](docs/api.md)
- CLI users: [CLI Guide](docs/cli.md)
- Contributors: [Architecture](docs/architecture.md)
- Methodology readers: [Methodology](docs/methodology.md)

---

## Command-Line Interface

EconKit includes a command-line interface.

### Validate a Dataset

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Checks whether the dataset has the required macroeconomic columns.

---

### Create a Data-Quality Profile

```bash
python src/econkit_cli.py profile data/sample_economic_data.csv --output-dir outputs/profile
```

Generates:

- `data_quality_report.md`
- `data_quality_report.json`

Useful for checking missing values, duplicate rows, year range, and column structure.

---

### Generate an Economic Report

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

Generates:

- Economic Markdown report
- Indicator charts
- Monetary policy report
- Data-quality report

---

### Analyze Macroeconomic Risk

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

Classifies:

- Inflation pressure
- Growth condition
- Labor market condition
- Monetary condition
- Overall macroeconomic risk

Example output:

```text
Macro risk analysis completed.
Overall macro risk: Moderate
Markdown summary saved to: outputs/risk/macro_risk_summary.md
JSON summary saved to: outputs/risk/macro_risk_summary.json
```

---

### Analyze Monetary Policy Stance

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
```

Compares:

- Actual interest rate
- Simple policy-rule benchmark
- Policy gap
- Real interest rate

Possible policy stance labels:

- `Tight`
- `Moderately Tight`
- `Neutral`
- `Moderately Accommodative`
- `Accommodative`

Custom assumptions:

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv \
  --output-dir outputs/policy \
  --target-inflation 2.0 \
  --neutral-interest-rate 2.5 \
  --potential-growth 2.0 \
  --inflation-weight 0.5 \
  --growth-weight 0.5
```

---

### Diagnose Business-Cycle Conditions

```bash
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
```

Possible cycle labels include:

- `Recession`
- `Slowdown`
- `Weak Recovery`
- `Recovery`
- `Stable Expansion`
- `Expansion`
- `Overheating`

---

### Diagnose Inflation Pressure

```bash
python src/econkit_cli.py inflation data/sample_economic_data.csv --output-dir outputs/inflation
```

Analyzes:

- Latest inflation rate
- Inflation gap relative to target
- Recent average inflation
- Inflation momentum
- Inflation pressure classification

Custom target:

```bash
python src/econkit_cli.py inflation data/sample_economic_data.csv \
  --output-dir outputs/inflation \
  --target-inflation 2.0 \
  --window 3
```

---

### Analyze the Policy Mix

```bash
python src/econkit_cli.py mix data/sample_economic_data.csv --output-dir outputs/mix
```

Combines:

- Macro risk
- Monetary policy stance
- Business-cycle phase
- Inflation pressure

Outputs a policy-mix regime such as:

- `Stable macro regime`
- `Mixed macro regime`
- `Elevated tension macro regime`
- `High tension macro regime`

---

### Generate Macro Scenarios

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

Default scenarios:

- `baseline`
- `inflation_shock`
- `recession_shock`
- `tight_policy`

Stress-test scenarios:

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv \
  --output-dir outputs/scenarios \
  --years 5 \
  --stress-tests
```

Stress-test scenarios include:

- `stagflation`
- `soft_landing`
- `hard_landing`
- `supply_recovery`
- `policy_mistake`

---

### Generate Forecasts

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv --output-dir outputs/forecasts --periods 5
```

Available methods:

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv \
  --output-dir outputs/forecasts \
  --method ar1 \
  --periods 5
```

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv \
  --output-dir outputs/forecasts \
  --method moving_average \
  --periods 5
```

Forecast selected columns:

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv \
  --output-dir outputs/forecasts \
  --columns gdp_growth inflation_rate
```

---

### Run OLS Regression

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression
```

With robust standard errors:

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression \
  --robust
```

Outputs:

- `regression_report.md`
- `regression_result.json`

---

### Generate a Full Analysis Package

```bash
python src/econkit_cli.py package data/sample_economic_data.csv --output-dir outputs/package --years 5
```

Creates a professional output package:

```text
outputs/package/
  data/
    cleaned_macro_data.csv
  charts/
    gdp_growth.png
    inflation_rate.png
    unemployment_rate.png
    interest_rate.png
    macro_indicators.png
  reports/
    economic_report.md
    monetary_policy_report.md
    data_quality_report.md
    diagnostics.json
  forecasts/
    indicator_forecasts.csv
  scenarios/
    baseline_scenario.csv
    stagflation_scenario.csv
    soft_landing_scenario.csv
    hard_landing_scenario.csv
    supply_recovery_scenario.csv
    policy_mistake_scenario.csv
    scenario_comparison.csv
    macro_scenario_report.md
```

---

### List Available Features

```bash
python src/econkit_cli.py features
```

---

## Python API Examples

EconKit can also be used directly from Python.

### Load and Analyze Data

```python
from econkit import (
    load_economic_data,
    clean_macro_dataset,
    analyze_macro_risk,
    analyze_monetary_policy_stance,
)

data = load_economic_data("data/sample_economic_data.csv")
data = clean_macro_dataset(data)

risk = analyze_macro_risk(data)
policy = analyze_monetary_policy_stance(data)

print(risk["summary"])
print(policy["summary"])
```

---

### Business-Cycle and Inflation Analysis

```python
from econkit import analyze_business_cycle, analyze_inflation_pressure

cycle = analyze_business_cycle(data)
inflation = analyze_inflation_pressure(data)

print(cycle["summary"])
print(inflation["summary"])
```

---

### Scenario Simulation

```python
from econkit import build_stress_test_scenarios, compare_macro_scenarios

scenarios = build_stress_test_scenarios(data, years=5)
comparison = compare_macro_scenarios(scenarios)

print(comparison)
```

---

### Forecasting

```python
from econkit import generate_forecast_table

forecasts = generate_forecast_table(
    data,
    columns=["gdp_growth", "inflation_rate"],
    periods=5,
    method="ar1",
)

print(forecasts)
```

---

### Regression

```python
from econkit import run_ols_formula, regression_report

result = run_ols_formula(
    data,
    "inflation_rate ~ gdp_growth + unemployment_rate",
    robust=True,
)

print(result.summary_frame())

regression_report(result, "outputs/regression_report.md")
```

---

## Core Functions

### Data Tools

| Function | Purpose |
|---|---|
| `load_economic_data` | Load CSV, Excel, Parquet, or JSON data |
| `save_dataset` | Save data to CSV, Excel, Parquet, or JSON |
| `clean_column_names` | Standardize column names |
| `clean_macro_dataset` | Prepare macroeconomic data for EconKit |
| `validate_macro_dataset` | Validate required macro columns |
| `profile_dataset` | Build a dataset profile |
| `data_quality_report` | Generate a quality report |

### Statistical Tools

| Function | Purpose |
|---|---|
| `calculate_summary_statistics` | Summary statistics |
| `calculate_average_growth` | Average indicator value |
| `calculate_correlation_matrix` | Correlation matrix |
| `calculate_rolling_statistics` | Rolling means and volatility |
| `calculate_growth_rates` | Percent growth rates |
| `calculate_z_scores` | Standardized z-scores |

### Chart Tools

| Function | Purpose |
|---|---|
| `create_line_chart` | Single indicator line chart |
| `create_multi_line_chart` | Multi-indicator line chart |
| `create_scatter_chart` | Two-variable scatter chart |

### Macro Diagnostics

| Function | Purpose |
|---|---|
| `analyze_macro_risk` | Overall macro risk analysis |
| `analyze_monetary_policy_stance` | Monetary policy stance analysis |
| `analyze_business_cycle` | Business-cycle diagnosis |
| `analyze_inflation_pressure` | Inflation pressure diagnosis |
| `analyze_policy_mix` | Integrated macro regime analysis |

### Scenarios and Forecasting

| Function | Purpose |
|---|---|
| `simulate_macro_scenario` | Simulate one macro scenario |
| `build_default_macro_scenarios` | Build baseline scenario set |
| `build_stress_test_scenarios` | Build stress-test scenario set |
| `compare_macro_scenarios` | Compare scenario outcomes |
| `forecast_ar1` | AR(1) forecast |
| `forecast_moving_average` | Moving-average forecast |
| `generate_forecast_table` | Multi-indicator forecast table |

### Econometrics

| Function | Purpose |
|---|---|
| `run_ols` | Run OLS regression |
| `parse_formula` | Parse a simple regression formula |
| `run_ols_formula` | Formula-based OLS |
| `regression_report` | Generate regression Markdown report |

### Reporting

| Function | Purpose |
|---|---|
| `generate_monetary_policy_report` | Monetary policy Markdown report |
| `generate_markdown_report` | Full economic report |
| `generate_economic_report` | Report and chart workflow |
| `generate_macro_scenario_report` | Scenario report |
| `generate_macro_scenario_analysis` | Scenario files and report |
| `generate_full_analysis_package` | Complete project output package |
| `quick_analyze` | Run key diagnostics in one call |
| `export_json` | Export diagnostics to JSON |

---

## Example Output Interpretation

A monetary policy result may look like:

```python
{
    "latest_year": 2024,
    "actual_interest_rate": 3.5,
    "recommended_policy_rate": 3.57,
    "policy_gap": -0.07,
    "real_interest_rate": 1.2,
    "policy_stance": "Neutral"
}
```

Interpretation:

```text
The actual interest rate is close to the policy-rule benchmark.
EconKit classifies monetary policy as Neutral.
```

A macro risk result may look like:

```python
{
    "latest_year": 2024,
    "overall_risk": "Moderate",
    "risk_score": 1,
    "signals": {
        "inflation_pressure": "Normal",
        "growth_condition": "Moderate",
        "labor_market": "Tight",
        "monetary_condition": "Tight"
    }
}
```

Interpretation:

```text
The economy is not in a high-risk regime, but tight monetary conditions create some macro risk.
```

---

## Testing

Run:

```bash
pytest
```

Expected result:

```text
passed
```

GitHub Actions is configured to run tests automatically.

---

## Project Structure

```text
econkit/
  .github/
    workflows/
      tests.yml
  data/
    sample_economic_data.csv
  docs/
    cli.md
  examples/
    analyze_macro_data.py
    analyze_macro_risk.py
    generate_report.py
    run_macro_scenarios.py
  outputs/
  src/
    econkit.py
    econkit_cli.py
  tests/
    test_cli.py
    test_econkit.py
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  LICENSE
  pyproject.toml
  requirements.txt
```

---

## Design Philosophy

EconKit is intentionally transparent.

Many professional economics tools are powerful but hard for beginners to understand. EconKit takes the opposite approach:

- Use readable formulas
- Use simple thresholds
- Generate interpretable outputs
- Keep the code inspectable
- Make analysis reproducible
- Help students learn by reading the output

The goal is not to replace advanced econometric software.

The goal is to help users build confidence moving from economic data to economic reasoning.

---

## Limitations

EconKit is useful for education, exploratory analysis, and lightweight applied workflows.

However:

- It is not a central-bank forecasting model.
- It is not a replacement for structural macroeconomic modeling.
- It is not a replacement for professional econometric packages.
- Its policy-rule analysis is simplified.
- Its scenario simulations are transparent teaching models, not official forecasts.
- Its OLS engine is lightweight and intentionally minimal.

Users should treat EconKit outputs as starting points for interpretation, not final policy conclusions.

---

## Roadmap

Possible future improvements:

- More datasets and examples
- More chart styles
- Panel-data tools
- Time-series diagnostics
- Forecast evaluation metrics
- Confidence intervals for forecasts
- More regression diagnostics
- Export to HTML
- Export to PDF
- Streamlit dashboard
- Jupyter notebook examples
- PyPI release
- Documentation website

---

## License

This project is licensed under the MIT License.

See [LICENSE](LICENSE).

---

## Citation

If you use EconKit for a class project, research prototype, or public analysis, you can cite it as:

```text
Lee, Gyujin. EconKit: A Python Toolkit for Beginner-Friendly Economics Data Analysis.
GitHub repository: https://github.com/car6770/econkit
```

---

## Author

Created by **Gyujin Lee**.

EconKit began as a beginner-friendly economics data analysis project and is evolving into a practical toolkit for macroeconomic diagnostics, reporting, scenario simulation, forecasting, and lightweight econometrics.
