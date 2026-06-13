# EconKit CLI Guide

This guide explains how to use the EconKit command-line interface.

The CLI is designed for users who want to run economics data analysis from a terminal or GitHub Codespaces without writing Python scripts.

---

## Basic Pattern

Most EconKit commands follow this structure:

```bash
python src/econkit_cli.py COMMAND data/sample_economic_data.csv --output-dir outputs/some_folder
```

The first argument is usually the dataset path.

The `--output-dir` option tells EconKit where to save reports, charts, JSON files, CSV files, and analysis outputs.

---

## Required Dataset Columns

The main macroeconomic workflow expects these columns:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

Example CSV:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
2020,-0.7,0.5,4.0,0.5
2021,4.3,2.5,3.7,1.0
2022,2.6,5.1,3.0,3.25
2023,1.4,3.6,2.7,3.50
2024,2.0,2.3,2.8,3.50
```

Column names are automatically cleaned into lowercase snake_case when possible.

For example:

```text
GDP Growth
GDP-Growth
GDP/Growth
```

can be cleaned into:

```text
gdp_growth
```

---

## 1. Validate a Dataset

Use `validate` to check whether a dataset can be used by EconKit.

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Expected output:

```text
Dataset validation passed.
Rows: 5
Columns: year, gdp_growth, inflation_rate, unemployment_rate, interest_rate
```

Use this command first when working with a new dataset.

---

## 2. Create a Data-Quality Profile

Use `profile` to create a data-quality report.

```bash
python src/econkit_cli.py profile data/sample_economic_data.csv --output-dir outputs/profile
```

Generated files:

```text
outputs/profile/data_quality_report.md
outputs/profile/data_quality_report.json
```

The profile checks:

- Number of rows
- Number of columns
- Column names
- Numeric columns
- Missing values
- Duplicate rows
- Year range
- Data-quality issues

This is useful before writing a report or running analysis.

---

## 3. Generate an Economic Report

Use `report` to generate the main EconKit economic report.

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

Generated outputs may include:

```text
outputs/report/economic_report.md
outputs/report/monetary_policy_report.md
outputs/report/data_quality_report.md
outputs/report/gdp_growth.png
outputs/report/inflation_rate.png
outputs/report/unemployment_rate.png
outputs/report/interest_rate.png
outputs/report/macro_indicators.png
```

This command is useful when you want a readable report and charts from one dataset.

---

## 4. Analyze Macroeconomic Risk

Use `risk` to classify macroeconomic risk.

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

Generated files:

```text
outputs/risk/macro_risk_summary.md
outputs/risk/macro_risk_summary.json
```

The macro risk model uses transparent rule-based signals:

| Signal | Input |
|---|---|
| Inflation pressure | `inflation_rate` |
| Growth condition | `gdp_growth` |
| Labor market condition | `unemployment_rate` |
| Monetary condition | `interest_rate` |

Possible overall risk labels:

```text
Low
Moderate
Elevated
High
```

Example output:

```text
Macro risk analysis completed.
Overall macro risk: Moderate
Markdown summary saved to: outputs/risk/macro_risk_summary.md
JSON summary saved to: outputs/risk/macro_risk_summary.json
```

---

## 5. Analyze Monetary Policy Stance

Use `policy` to compare the actual interest rate with a transparent policy-rule benchmark.

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
```

Generated files:

```text
outputs/policy/monetary_policy_summary.md
outputs/policy/monetary_policy_summary.json
outputs/policy/monetary_policy_report.md
```

The policy analysis compares:

```text
actual interest rate
policy-rule benchmark rate
policy gap
real interest rate
```

Possible policy stance labels:

```text
Tight
Moderately Tight
Neutral
Moderately Accommodative
Accommodative
```

### Custom Policy Assumptions

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv \
  --output-dir outputs/policy \
  --target-inflation 2.0 \
  --neutral-interest-rate 2.5 \
  --potential-growth 2.0 \
  --inflation-weight 0.5 \
  --growth-weight 0.5
```

Explanation:

| Option | Meaning |
|---|---|
| `--target-inflation` | Inflation target used in the policy rule |
| `--neutral-interest-rate` | Assumed neutral interest rate |
| `--potential-growth` | Assumed potential GDP growth |
| `--inflation-weight` | Weight on inflation gap |
| `--growth-weight` | Weight on growth gap |

---

## 6. Diagnose Business-Cycle Conditions

Use `cycle` to classify the latest business-cycle condition.

```bash
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
```

Generated files:

```text
outputs/cycle/business_cycle_summary.md
outputs/cycle/business_cycle_summary.json
```

Possible labels include:

```text
Recession
Slowdown
Weak Recovery
Recovery
Stable Expansion
Expansion
Overheating
```

This diagnosis uses GDP growth, an estimated potential growth benchmark, an output-gap proxy, and inflation information.

---

## 7. Diagnose Inflation Pressure

Use `inflation` to analyze inflation pressure and momentum.

```bash
python src/econkit_cli.py inflation data/sample_economic_data.csv --output-dir outputs/inflation
```

Generated files:

```text
outputs/inflation/inflation_pressure_summary.md
outputs/inflation/inflation_pressure_summary.json
```

The inflation diagnosis includes:

```text
latest inflation rate
target inflation
inflation gap
recent average inflation
inflation momentum
inflation pressure label
```

### Custom Inflation Target

```bash
python src/econkit_cli.py inflation data/sample_economic_data.csv \
  --output-dir outputs/inflation \
  --target-inflation 2.0 \
  --window 3
```

Explanation:

| Option | Meaning |
|---|---|
| `--target-inflation` | Inflation target |
| `--window` | Number of recent observations used for recent average inflation |

---

## 8. Analyze the Macro Policy Mix

Use `mix` to combine several diagnostics into a single macro regime.

```bash
python src/econkit_cli.py mix data/sample_economic_data.csv --output-dir outputs/mix
```

Generated files:

```text
outputs/mix/policy_mix_summary.md
outputs/mix/policy_mix_summary.json
```

The policy-mix analysis combines:

```text
macro risk
monetary policy stance
business-cycle phase
inflation pressure
```

Possible regime labels:

```text
Stable macro regime
Mixed macro regime
Elevated tension macro regime
High tension macro regime
```

---

## 9. Generate Macro Scenarios

Use `scenarios` to simulate future macroeconomic paths.

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

Generated files:

```text
outputs/scenarios/baseline_scenario.csv
outputs/scenarios/inflation_shock_scenario.csv
outputs/scenarios/recession_shock_scenario.csv
outputs/scenarios/tight_policy_scenario.csv
outputs/scenarios/scenario_comparison.csv
outputs/scenarios/macro_scenario_report.md
```

Default scenarios:

| Scenario | Meaning |
|---|---|
| `baseline` | Continuation of recent macro conditions |
| `inflation_shock` | Supply-side inflation shock |
| `recession_shock` | Negative demand shock |
| `tight_policy` | Higher interest-rate shock |

### Stress-Test Scenarios

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv \
  --output-dir outputs/scenarios \
  --years 5 \
  --stress-tests
```

Stress-test scenarios include:

| Scenario | Meaning |
|---|---|
| `stagflation` | Weak demand plus high supply shock |
| `soft_landing` | Mild demand adjustment with lower inflation pressure |
| `hard_landing` | Strong negative demand shock |
| `supply_recovery` | Improvement in supply-side conditions |
| `policy_mistake` | Weak demand plus excessive tightening |

---

## 10. Generate Forecasts

Use `forecast` to create simple indicator forecasts.

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv --output-dir outputs/forecasts --periods 5
```

Generated file:

```text
outputs/forecasts/indicator_forecasts.csv
```

Available methods:

```text
ar1
moving_average
```

### AR(1) Forecast

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv \
  --output-dir outputs/forecasts \
  --method ar1 \
  --periods 5
```

### Moving-Average Forecast

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv \
  --output-dir outputs/forecasts \
  --method moving_average \
  --periods 5
```

### Forecast Selected Columns

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv \
  --output-dir outputs/forecasts \
  --columns gdp_growth inflation_rate
```

---

## 11. Run OLS Regression

Use `ols` to run lightweight ordinary least squares regression.

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression
```

Generated files:

```text
outputs/regression/regression_report.md
outputs/regression/regression_result.json
```

### Robust Standard Errors

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression \
  --robust
```

Formula format:

```text
dependent_variable ~ independent_variable_1 + independent_variable_2
```

Examples:

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "gdp_growth ~ interest_rate + inflation_rate" \
  --output-dir outputs/regression
```

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "unemployment_rate ~ gdp_growth + interest_rate" \
  --output-dir outputs/regression
```

---

## 12. Generate a Full Analysis Package

Use `package` to generate a professional analysis folder.

```bash
python src/econkit_cli.py package data/sample_economic_data.csv --output-dir outputs/package --years 5
```

Generated structure:

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

This is one of the most useful commands when preparing a complete project output.

---

## 13. List Available Features

Use `features` to print EconKit's feature list.

```bash
python src/econkit_cli.py features
```

Example output:

```text
Available EconKit features:
- dataset loading
- dataset cleaning
- dataset validation
- data quality report
- summary statistics
- correlation matrix
- rolling statistics
- z-scores
- line charts
- multi-line charts
- scatter charts
- macro risk analysis
- monetary policy stance analysis
- business-cycle diagnosis
- inflation pressure diagnosis
- policy-mix analysis
- scenario simulation
- stress-test scenarios
- AR(1) forecasting
- moving-average forecasting
- OLS regression
- formula regression
- robust standard errors
- Markdown reports
- full analysis package
```

---

## 14. Run the Main Workflow

Use `all` to run the main EconKit workflow.

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

With stress-test scenarios:

```bash
python src/econkit_cli.py all data/sample_economic_data.csv \
  --output-dir outputs \
  --years 5 \
  --stress-tests
```

Generated folders:

```text
outputs/
  report/
  risk/
  policy/
  cycle/
  inflation/
  mix/
  scenarios/
  forecasts/
```

This command is the easiest way to generate a complete macroeconomic analysis.

---

## Recommended Workflow

For a new dataset, use this sequence:

```bash
python src/econkit_cli.py validate data/my_data.csv
python src/econkit_cli.py profile data/my_data.csv --output-dir outputs/profile
python src/econkit_cli.py all data/my_data.csv --output-dir outputs --years 5 --stress-tests
```

For a policy-focused project:

```bash
python src/econkit_cli.py policy data/my_data.csv --output-dir outputs/policy
python src/econkit_cli.py inflation data/my_data.csv --output-dir outputs/inflation
python src/econkit_cli.py cycle data/my_data.csv --output-dir outputs/cycle
python src/econkit_cli.py mix data/my_data.csv --output-dir outputs/mix
```

For a forecasting and scenario project:

```bash
python src/econkit_cli.py forecast data/my_data.csv --output-dir outputs/forecasts --periods 5
python src/econkit_cli.py scenarios data/my_data.csv --output-dir outputs/scenarios --years 5 --stress-tests
```

For an econometrics project:

```bash
python src/econkit_cli.py ols data/my_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression \
  --robust
```

---

## Troubleshooting

### Error: Missing required columns

Example:

```text
ValueError: Missing required columns: ['gdp_growth']
```

Fix:

Check that the dataset contains:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

Also check spelling.

---

### Error: Dataset not found

Example:

```text
FileNotFoundError: Dataset not found: data/sample_economic_data.csv
```

Fix:

Make sure the file path is correct.

If your file is in the `data` folder:

```bash
python src/econkit_cli.py validate data/your_file.csv
```

---

### Error: duplicate years

Example:

```text
ValueError: Column 'year' contains duplicate years.
```

Fix:

Use one observation per year for the main macro workflow.

---

### Error: missing values

Example:

```text
ValueError: Column 'inflation_rate' contains 1 missing values.
```

Fix:

Fill or remove missing values before running the main workflow.

---

### Command not found

If this does not work:

```bash
econkit validate data/sample_economic_data.csv
```

use this instead:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

The direct Python command works without installing the package as a console command.

---

## Notes on Interpretation

EconKit is designed for transparent analysis.

Its macro risk, policy stance, business-cycle, inflation, forecasting, and scenario tools are useful for:

- learning
- exploratory analysis
- class projects
- research prototypes
- policy memo drafts
- reproducible workflows

They are not official forecasts or policy recommendations.

Use EconKit outputs as structured starting points for economic reasoning.

---

## Quick Reference

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
python src/econkit_cli.py profile data/sample_economic_data.csv --output-dir outputs/profile
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
python src/econkit_cli.py inflation data/sample_economic_data.csv --output-dir outputs/inflation
python src/econkit_cli.py mix data/sample_economic_data.csv --output-dir outputs/mix
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5 --stress-tests
python src/econkit_cli.py forecast data/sample_economic_data.csv --output-dir outputs/forecasts --periods 5
python src/econkit_cli.py ols data/sample_economic_data.csv --formula "inflation_rate ~ gdp_growth + unemployment_rate" --output-dir outputs/regression
python src/econkit_cli.py package data/sample_economic_data.csv --output-dir outputs/package --years 5
python src/econkit_cli.py features
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5 --stress-tests
```
