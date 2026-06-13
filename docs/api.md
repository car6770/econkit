# EconKit API Reference

This document provides a practical reference for EconKit's Python API.

EconKit is organized around a simple workflow:

```text
load data
clean data
validate data
analyze data
generate reports
export outputs
```

The main source file is:

```text
src/econkit.py
```

---

## Import Pattern

When using EconKit from a script after installing the package:

```python
from econkit import load_economic_data, analyze_macro_risk
```

When running examples directly from the repository, example files usually add the `src` folder to the Python path:

```python
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))
```

---

## Required Macro Dataset Format

Most macroeconomic diagnostic functions expect a pandas DataFrame with these columns:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

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

# Data Loading and Saving

## `load_economic_data(file_path)`

Load an economic dataset.

Supported file formats:

```text
.csv
.xlsx
.xls
.parquet
.json
```

Example:

```python
from econkit import load_economic_data

data = load_economic_data("data/sample_economic_data.csv")
```

Returns:

```text
pandas.DataFrame
```

Raises:

```text
FileNotFoundError
ValueError for unsupported file types
```

---

## `save_dataset(data, file_path, index=False)`

Save a pandas DataFrame.

Example:

```python
from econkit import save_dataset

save_dataset(data, "outputs/cleaned_data.csv")
```

Supported output formats:

```text
.csv
.xlsx
.xls
.parquet
.json
```

Returns:

```text
pathlib.Path
```

---

# Data Cleaning and Validation

## `clean_column_names(data)`

Standardize column names into lowercase snake-style names.

Example:

```python
from econkit import clean_column_names

cleaned = clean_column_names(data)
```

Example transformation:

```text
GDP Growth -> gdp_growth
Inflation Rate -> inflation_rate
Interest-Rate -> interest_rate
```

Returns:

```text
pandas.DataFrame
```

---

## `coerce_numeric_columns(data, columns=None, errors="coerce")`

Convert selected columns to numeric values.

Example:

```python
from econkit import coerce_numeric_columns

cleaned = coerce_numeric_columns(
    data,
    columns=["gdp_growth", "inflation_rate"],
)
```

If `columns=None`, EconKit tries to convert all columns.

Returns:

```text
pandas.DataFrame
```

---

## `clean_macro_dataset(data)`

Clean a macroeconomic dataset for EconKit analysis.

This function:

- standardizes column names
- converts required macro columns to numeric values
- converts year to integer
- sorts by year
- drops duplicate years by keeping the latest row

Example:

```python
from econkit import clean_macro_dataset, load_economic_data

data = load_economic_data("data/sample_economic_data.csv")
data = clean_macro_dataset(data)
```

Returns:

```text
pandas.DataFrame
```

---

## `validate_macro_dataset(data, required_columns=REQUIRED_MACRO_COLUMNS, allow_missing=False)`

Validate that a dataset is usable by EconKit's macro workflow.

Example:

```python
from econkit import validate_macro_dataset

validate_macro_dataset(data)
```

Returns:

```text
True
```

Raises:

```text
ValueError
```

Common validation errors:

```text
Missing required columns
Dataset is empty
Column contains missing values
Year column contains non-numeric values
Year column contains duplicate years
```

---

## `profile_dataset(data)`

Create a compact dataset profile.

Example:

```python
from econkit import profile_dataset

profile = profile_dataset(data)

print(profile.rows)
print(profile.columns)
print(profile.numeric_columns)
```

Returns:

```text
DatasetProfile
```

The profile includes:

```text
rows
columns
column_names
numeric_columns
missing_values
duplicate_rows
year_min
year_max
issues
```

---

## `data_quality_report(data, output_path=None)`

Create a data-quality report.

Example:

```python
from econkit import data_quality_report

report = data_quality_report(
    data,
    output_path="outputs/data_quality_report.md",
)
```

Returns:

```text
dict
```

Optional output:

```text
Markdown report
```

---

# Basic Statistics

## `calculate_summary_statistics(data)`

Calculate summary statistics using pandas.

Example:

```python
from econkit import calculate_summary_statistics

summary = calculate_summary_statistics(data)
print(summary)
```

Returns:

```text
pandas.DataFrame
```

---

## `calculate_average_growth(data, column)`

Calculate the average value of a selected economic indicator.

Example:

```python
from econkit import calculate_average_growth

avg_growth = calculate_average_growth(data, "gdp_growth")
```

Returns:

```text
float
```

---

## `find_highest_value_year(data, column)`

Find the row with the highest value for a selected indicator.

Example:

```python
from econkit import find_highest_value_year

highest = find_highest_value_year(data, "inflation_rate")
print(highest["year"])
```

Returns:

```text
pandas.Series
```

---

## `find_lowest_value_year(data, column)`

Find the row with the lowest value for a selected indicator.

Example:

```python
from econkit import find_lowest_value_year

lowest = find_lowest_value_year(data, "inflation_rate")
print(lowest["year"])
```

Returns:

```text
pandas.Series
```

---

## `calculate_correlation_matrix(data, columns)`

Calculate a correlation matrix.

Example:

```python
from econkit import calculate_correlation_matrix

corr = calculate_correlation_matrix(
    data,
    ["gdp_growth", "inflation_rate", "unemployment_rate"],
)
```

Returns:

```text
pandas.DataFrame
```

---

## `calculate_rolling_statistics(data, column, window=3, statistics=("mean", "std"))`

Add rolling statistics for a selected column.

Example:

```python
from econkit import calculate_rolling_statistics

rolling = calculate_rolling_statistics(
    data,
    column="inflation_rate",
    window=3,
)
```

Possible statistics:

```text
mean
std
min
max
```

Returns:

```text
pandas.DataFrame
```

---

## `calculate_growth_rates(data, column, periods=1, multiply_by_100=True)`

Calculate percent growth rates for a level variable.

Example:

```python
from econkit import calculate_growth_rates

data["gdp_level_growth"] = calculate_growth_rates(data, "gdp_level")
```

Returns:

```text
pandas.Series
```

---

## `calculate_z_scores(data, columns)`

Add z-score columns for selected indicators.

Example:

```python
from econkit import calculate_z_scores

data_with_z = calculate_z_scores(
    data,
    ["gdp_growth", "inflation_rate"],
)
```

New columns:

```text
gdp_growth_zscore
inflation_rate_zscore
```

Returns:

```text
pandas.DataFrame
```

---

# Charts

## `create_line_chart(data, x_column, y_column, output_path, title=None)`

Create and save a line chart.

Example:

```python
from econkit import create_line_chart

create_line_chart(
    data=data,
    x_column="year",
    y_column="gdp_growth",
    output_path="outputs/gdp_growth.png",
    title="GDP Growth Over Time",
)
```

Returns:

```text
pathlib.Path
```

---

## `create_multi_line_chart(data, x_column, y_columns, output_path, title="Economic Indicators Over Time")`

Create and save a multi-line chart.

Example:

```python
from econkit import create_multi_line_chart

create_multi_line_chart(
    data=data,
    x_column="year",
    y_columns=["gdp_growth", "inflation_rate", "unemployment_rate"],
    output_path="outputs/macro_indicators.png",
)
```

Returns:

```text
pathlib.Path
```

---

## `create_scatter_chart(data, x_column, y_column, output_path, title=None)`

Create and save a scatter chart.

Example:

```python
from econkit import create_scatter_chart

create_scatter_chart(
    data=data,
    x_column="gdp_growth",
    y_column="inflation_rate",
    output_path="outputs/growth_vs_inflation.png",
)
```

Returns:

```text
pathlib.Path
```

---

# Macro Risk Analysis

## `classify_inflation_pressure(inflation_rate)`

Classify inflation pressure.

Possible outputs:

```text
Low
Normal
Elevated
High
Unknown
```

Example:

```python
from econkit import classify_inflation_pressure

label = classify_inflation_pressure(3.2)
```

---

## `classify_growth_condition(gdp_growth)`

Classify GDP growth condition.

Possible outputs:

```text
Contraction
Weak
Moderate
Strong
Unknown
```

---

## `classify_labor_market(unemployment_rate)`

Classify labor-market condition.

Possible outputs:

```text
Tight
Stable
Soft
Weak
Unknown
```

---

## `classify_monetary_condition(interest_rate)`

Classify monetary condition.

Possible outputs:

```text
Accommodative
Neutral
Tight
Unknown
```

---

## `calculate_macro_risk_score(signals)`

Calculate a macro risk score from classified signals.

Example:

```python
from econkit import calculate_macro_risk_score

score = calculate_macro_risk_score(
    {
        "inflation_pressure": "Elevated",
        "growth_condition": "Weak",
        "labor_market": "Stable",
        "monetary_condition": "Tight",
    }
)
```

Returns:

```text
int
```

---

## `classify_overall_macro_risk(score)`

Classify overall macro risk from a numeric score.

Possible outputs:

```text
Low
Moderate
Elevated
High
```

---

## `analyze_macro_risk(data)`

Run the full macro risk analysis.

Example:

```python
from econkit import analyze_macro_risk

risk = analyze_macro_risk(data)

print(risk["overall_risk"])
print(risk["summary"])
```

Returns:

```python
{
    "latest_year": 2024,
    "latest_values": {
        "gdp_growth": 2.0,
        "inflation_rate": 2.3,
        "unemployment_rate": 2.8,
        "interest_rate": 3.5,
    },
    "signals": {
        "inflation_pressure": "Normal",
        "growth_condition": "Moderate",
        "labor_market": "Tight",
        "monetary_condition": "Tight",
    },
    "risk_score": 1,
    "overall_risk": "Moderate",
    "summary": "..."
}
```

---

# Monetary Policy Analysis

## `estimate_macro_baseline(data, window=5)`

Estimate baseline macro values from recent data.

Example:

```python
from econkit import estimate_macro_baseline

baseline = estimate_macro_baseline(data)
```

Returns:

```python
{
    "potential_growth": 2.0,
    "target_inflation": 2.0,
    "normal_unemployment": 3.2,
    "neutral_interest_rate": 2.5,
}
```

---

## `calculate_real_interest_rate(nominal_interest_rate, inflation_rate, exact=False)`

Calculate the real interest rate.

Approximate method:

```text
real interest rate = nominal interest rate - inflation rate
```

Example:

```python
from econkit import calculate_real_interest_rate

real_rate = calculate_real_interest_rate(3.5, 2.3)
```

---

## `calculate_policy_rule_rate(...)`

Calculate a transparent policy-rule benchmark interest rate.

Formula:

```text
policy rule rate =
neutral interest rate
+ inflation weight × inflation gap
+ growth weight × growth gap
```

Example:

```python
from econkit import calculate_policy_rule_rate

rate = calculate_policy_rule_rate(
    inflation_rate=3.0,
    gdp_growth=2.5,
    target_inflation=2.0,
    neutral_interest_rate=2.0,
    potential_growth=2.0,
)
```

Returns:

```text
float
```

---

## `classify_policy_stance(policy_gap)`

Classify monetary policy stance.

The policy gap is:

```text
actual interest rate - policy rule benchmark rate
```

Possible outputs:

```text
Tight
Moderately Tight
Neutral
Moderately Accommodative
Accommodative
```

---

## `analyze_monetary_policy_stance(data, ...)`

Analyze monetary policy stance.

Example:

```python
from econkit import analyze_monetary_policy_stance

policy = analyze_monetary_policy_stance(data)

print(policy["policy_stance"])
print(policy["summary"])
```

Optional arguments:

```text
target_inflation
neutral_interest_rate
potential_growth
inflation_weight
growth_weight
```

Returns:

```python
{
    "latest_year": 2024,
    "actual_interest_rate": 3.5,
    "recommended_policy_rate": 3.57,
    "policy_gap": -0.07,
    "real_interest_rate": 1.2,
    "policy_stance": "Neutral",
    "inputs": {...},
    "gaps": {...},
    "summary": "..."
}
```

---

# Business Cycle and Inflation

## `calculate_output_gap(data, gdp_growth_column="gdp_growth", potential_growth=None, window=5)`

Calculate a simple output-gap proxy.

Example:

```python
from econkit import calculate_output_gap

output_gap = calculate_output_gap(data)
```

Returns:

```text
pandas.Series
```

---

## `classify_business_cycle_phase(gdp_growth, output_gap, inflation_rate=None)`

Classify a simple business-cycle phase.

Possible outputs:

```text
Recession
Slowdown
Weak Recovery
Recovery
Stable Expansion
Expansion
Overheating
```

---

## `analyze_business_cycle(data)`

Diagnose the latest business-cycle condition.

Example:

```python
from econkit import analyze_business_cycle

cycle = analyze_business_cycle(data)

print(cycle["phase"])
print(cycle["summary"])
```

Returns keys such as:

```text
latest_year
phase
business_cycle_phase
gdp_growth
estimated_potential_growth
output_gap_proxy
inflation_rate
unemployment_rate
inflation_diagnosis
summary
```

Compatibility note:

```text
phase and business_cycle_phase are both supported.
```

---

## `analyze_inflation_pressure(data, target_inflation=2.0, window=3)`

Analyze inflation pressure and momentum.

Example:

```python
from econkit import analyze_inflation_pressure

inflation = analyze_inflation_pressure(data)

print(inflation["pressure"])
print(inflation["summary"])
```

Returns keys such as:

```text
latest_year
inflation_rate
target_inflation
inflation_gap
recent_average_inflation
inflation_momentum
momentum_label
pressure
summary
```

---

## `analyze_policy_mix(data)`

Combine macro risk, monetary policy, business cycle, and inflation diagnostics.

Example:

```python
from econkit import analyze_policy_mix

mix = analyze_policy_mix(data)

print(mix["regime"])
print(mix["summary"])
```

Possible regimes:

```text
Stable macro regime
Mixed macro regime
Elevated tension macro regime
High tension macro regime
```

---

# Scenario Simulation

## `simulate_macro_scenario(data, scenario_name, years=5, demand_shock=0.0, supply_shock=0.0, policy_shock=0.0)`

Simulate one macroeconomic scenario.

Example:

```python
from econkit import simulate_macro_scenario

scenario = simulate_macro_scenario(
    data,
    scenario_name="custom_recession",
    years=5,
    demand_shock=-2.0,
)
```

Returns:

```text
pandas.DataFrame
```

Scenario output columns:

```text
scenario
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

---

## `build_default_macro_scenarios(data, years=5)`

Build the default scenario set.

Scenarios:

```text
baseline
inflation_shock
recession_shock
tight_policy
```

Example:

```python
from econkit import build_default_macro_scenarios

scenarios = build_default_macro_scenarios(data, years=5)
```

Returns:

```text
dict[str, pandas.DataFrame]
```

---

## `build_stress_test_scenarios(data, years=5)`

Build stress-test scenarios.

Scenarios:

```text
baseline
stagflation
soft_landing
hard_landing
supply_recovery
policy_mistake
```

Example:

```python
from econkit import build_stress_test_scenarios

scenarios = build_stress_test_scenarios(data, years=5)
```

---

## `compare_macro_scenarios(scenarios)`

Compare final-year outcomes across scenarios.

Example:

```python
from econkit import compare_macro_scenarios

comparison = compare_macro_scenarios(scenarios)
```

Returns:

```text
pandas.DataFrame
```

Comparison columns:

```text
scenario
final_year
final_gdp_growth
final_inflation_rate
final_unemployment_rate
final_interest_rate
overall_risk
risk_score
```

---

# Forecasting

## `forecast_ar1(data, column, periods=5, year_column="year")`

Forecast one indicator using a simple AR(1) model.

Example:

```python
from econkit import forecast_ar1

forecast = forecast_ar1(data, "gdp_growth", periods=5)
```

Returns:

```text
pandas.DataFrame
```

Output columns:

```text
year
variable
forecast
model
intercept
phi
```

---

## `forecast_moving_average(data, column, periods=5, window=3, year_column="year")`

Forecast one indicator using a recent moving average.

Example:

```python
from econkit import forecast_moving_average

forecast = forecast_moving_average(
    data,
    "inflation_rate",
    periods=5,
    window=3,
)
```

---

## `generate_forecast_table(data, columns=DEFAULT_INDICATORS, periods=5, method="ar1")`

Generate forecasts for multiple indicators.

Example:

```python
from econkit import generate_forecast_table

forecasts = generate_forecast_table(
    data,
    columns=["gdp_growth", "inflation_rate"],
    periods=5,
    method="ar1",
)
```

Available methods:

```text
ar1
moving_average
```

---

# Lightweight Econometrics

## `parse_formula(formula)`

Parse a simple regression formula.

Example:

```python
from econkit import parse_formula

y, x = parse_formula("inflation_rate ~ gdp_growth + unemployment_rate")
```

Returns:

```python
("inflation_rate", ["gdp_growth", "unemployment_rate"])
```

---

## `run_ols(data, y_column, x_columns, add_constant=True, robust=False)`

Run ordinary least squares regression.

Example:

```python
from econkit import run_ols

result = run_ols(
    data,
    y_column="inflation_rate",
    x_columns=["gdp_growth", "unemployment_rate"],
    robust=True,
)
```

Returns:

```text
OLSResult
```

The `OLSResult` object includes:

```text
dependent_variable
independent_variables
coefficients
standard_errors
t_statistics
residuals
fitted_values
r_squared
adjusted_r_squared
nobs
df_model
df_resid
```

---

## `run_ols_formula(data, formula, add_constant=True, robust=False)`

Run OLS using a simple formula interface.

Example:

```python
from econkit import run_ols_formula

result = run_ols_formula(
    data,
    "inflation_rate ~ gdp_growth + unemployment_rate",
    robust=True,
)
```

---

## `regression_report(result, output_path=None)`

Generate a Markdown regression report.

Example:

```python
from econkit import regression_report

regression_report(
    result,
    output_path="outputs/regression_report.md",
)
```

Returns:

```text
str
```

If `output_path` is given, saves a Markdown report.

---

# Reports and Packages

## `generate_monetary_policy_report(data, output_path)`

Generate a monetary policy Markdown report.

Example:

```python
from econkit import generate_monetary_policy_report

generate_monetary_policy_report(
    data,
    "outputs/monetary_policy_report.md",
)
```

Returns:

```text
pathlib.Path
```

---

## `generate_markdown_report(data, indicators, output_path)`

Generate a full economic Markdown report.

Example:

```python
from econkit import generate_markdown_report

generate_markdown_report(
    data,
    indicators=["gdp_growth", "inflation_rate", "unemployment_rate", "interest_rate"],
    output_path="outputs/economic_report.md",
)
```

---

## `generate_economic_report(data_path, output_dir)`

Generate a report and charts from a dataset path.

Example:

```python
from econkit import generate_economic_report

generate_economic_report(
    "data/sample_economic_data.csv",
    "outputs/report",
)
```

Generated outputs may include:

```text
economic_report.md
monetary_policy_report.md
data_quality_report.md
gdp_growth.png
inflation_rate.png
unemployment_rate.png
interest_rate.png
macro_indicators.png
```

---

## `generate_macro_scenario_report(scenarios, output_path)`

Generate a Markdown scenario comparison report.

Example:

```python
from econkit import generate_macro_scenario_report

generate_macro_scenario_report(
    scenarios,
    "outputs/macro_scenario_report.md",
)
```

---

## `generate_macro_scenario_analysis(data_path, output_dir, years=5, stress_tests=False)`

Generate scenario CSV files, comparison data, and a Markdown report.

Example:

```python
from econkit import generate_macro_scenario_analysis

results = generate_macro_scenario_analysis(
    data_path="data/sample_economic_data.csv",
    output_dir="outputs/scenarios",
    years=5,
    stress_tests=True,
)
```

Returns:

```python
{
    "scenario_paths": {...},
    "comparison_path": Path(...),
    "report_path": Path(...),
}
```

---

## `generate_full_analysis_package(data_path, output_dir, years=5)`

Generate a full professional analysis package.

Example:

```python
from econkit import generate_full_analysis_package

results = generate_full_analysis_package(
    data_path="data/sample_economic_data.csv",
    output_dir="outputs/package",
    years=5,
)
```

Generated structure:

```text
outputs/package/
  data/
  charts/
  reports/
  forecasts/
  scenarios/
```

Returns:

```text
dict
```

---

# Convenience Helpers

## `quick_analyze(data_path)`

Run the main diagnostics in one call.

Example:

```python
from econkit import quick_analyze

diagnostics = quick_analyze("data/sample_economic_data.csv")
```

Returns:

```python
{
    "macro_risk": {...},
    "monetary_policy": {...},
    "business_cycle": {...},
    "inflation_pressure": {...},
    "policy_mix": {...},
}
```

---

## `export_json(data, output_path)`

Export a dictionary-like object as JSON.

Example:

```python
from econkit import export_json

export_json(
    diagnostics,
    "outputs/diagnostics.json",
)
```

Returns:

```text
pathlib.Path
```

---

## `list_available_features()`

Return a list of EconKit capabilities.

Example:

```python
from econkit import list_available_features

for feature in list_available_features():
    print(feature)
```

Returns:

```text
list[str]
```

---

# Data Classes

## `DataQualityIssue`

Represents one data-quality issue.

Fields:

```text
issue_type
column
message
severity
```

---

## `DatasetProfile`

Represents a compact profile of a dataset.

Fields:

```text
rows
columns
column_names
numeric_columns
missing_values
duplicate_rows
year_min
year_max
issues
```

---

## `OLSResult`

Represents an OLS regression result.

Fields:

```text
dependent_variable
independent_variables
coefficients
standard_errors
t_statistics
residuals
fitted_values
r_squared
adjusted_r_squared
nobs
df_model
df_resid
```

Methods:

```text
to_dict()
summary_frame()
```

Example:

```python
result = run_ols_formula(
    data,
    "inflation_rate ~ gdp_growth + unemployment_rate",
)

print(result.to_dict())
print(result.summary_frame())
```

---

# Recommended API Workflows

## Workflow 1: Basic Data Analysis

```python
from econkit import (
    load_economic_data,
    clean_macro_dataset,
    validate_macro_dataset,
    calculate_summary_statistics,
    calculate_correlation_matrix,
)

data = load_economic_data("data/sample_economic_data.csv")
data = clean_macro_dataset(data)
validate_macro_dataset(data)

summary = calculate_summary_statistics(data)
corr = calculate_correlation_matrix(
    data,
    ["gdp_growth", "inflation_rate", "unemployment_rate", "interest_rate"],
)
```

---

## Workflow 2: Macro Diagnostics

```python
from econkit import (
    analyze_macro_risk,
    analyze_monetary_policy_stance,
    analyze_business_cycle,
    analyze_inflation_pressure,
    analyze_policy_mix,
)

risk = analyze_macro_risk(data)
policy = analyze_monetary_policy_stance(data)
cycle = analyze_business_cycle(data)
inflation = analyze_inflation_pressure(data)
mix = analyze_policy_mix(data)
```

---

## Workflow 3: Scenarios and Forecasts

```python
from econkit import (
    build_stress_test_scenarios,
    compare_macro_scenarios,
    generate_forecast_table,
)

scenarios = build_stress_test_scenarios(data, years=5)
comparison = compare_macro_scenarios(scenarios)

forecasts = generate_forecast_table(
    data,
    columns=["gdp_growth", "inflation_rate"],
    periods=5,
)
```

---

## Workflow 4: Regression

```python
from econkit import run_ols_formula, regression_report

result = run_ols_formula(
    data,
    "inflation_rate ~ gdp_growth + unemployment_rate",
    robust=True,
)

regression_report(result, "outputs/regression_report.md")
```

---

## Workflow 5: Full Analysis Package

```python
from econkit import generate_full_analysis_package

generate_full_analysis_package(
    "data/sample_economic_data.csv",
    "outputs/package",
    years=5,
)
```

---

# Interpretation Warnings

EconKit is designed for educational and exploratory economic analysis.

The following tools are simplified and transparent:

```text
macro risk analysis
monetary policy stance analysis
business-cycle diagnosis
inflation pressure diagnosis
scenario simulation
forecasting
OLS regression
```

They should not be interpreted as:

```text
official forecasts
investment advice
central-bank decisions
professional policy recommendations
proof of causality
```

Use EconKit outputs as structured starting points for economic reasoning.
