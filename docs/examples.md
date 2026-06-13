# EconKit Examples Guide

This guide explains the example scripts included in EconKit.

The examples are designed to help users learn how EconKit works without needing to understand the whole codebase at once.

Each example can be run from the project root.

---

## Example Folder

Example scripts are stored in:

```text
examples/
```

Recommended structure:

```text
examples/
  analyze_macro_data.py
  analyze_macro_risk.py
  generate_report.py
  run_macro_scenarios.py
  run_forecasting.py
  run_regression.py
```

Each script uses:

```text
data/sample_economic_data.csv
```

and saves outputs under:

```text
outputs/examples/
```

---

## Before Running Examples

Install dependencies:

```bash
pip install -r requirements.txt
```

Then confirm the test suite works:

```bash
pytest
```

Then validate the sample dataset:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Expected output:

```text
Dataset validation passed.
```

---

## Example Dataset

The examples use a sample macroeconomic dataset with these columns:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

Example rows:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
2020,-0.7,0.5,4.0,0.5
2021,4.3,2.5,3.7,1.0
2022,2.6,5.1,3.0,3.25
2023,1.4,3.6,2.7,3.50
2024,2.0,2.3,2.8,3.50
```

The sample dataset is intentionally small and readable.

It is useful for:

- testing the project
- learning the API
- generating reports
- demonstrating charts
- demonstrating macro diagnostics
- demonstrating scenarios
- demonstrating forecasting
- demonstrating regression

---

# 1. Basic Macro Data Analysis

Script:

```text
examples/analyze_macro_data.py
```

Run:

```bash
python examples/analyze_macro_data.py
```

This example demonstrates basic EconKit analysis.

It loads the sample dataset, cleans it, validates it, calculates summary statistics, calculates a correlation matrix, and creates charts.

Generated outputs:

```text
outputs/examples/macro_data_summary.md
outputs/examples/correlation_matrix.csv
outputs/examples/gdp_growth_chart.png
outputs/examples/inflation_rate_chart.png
outputs/examples/macro_indicators_chart.png
```

Main EconKit functions used:

```python
load_economic_data
clean_macro_dataset
validate_macro_dataset
calculate_summary_statistics
calculate_correlation_matrix
calculate_average_growth
find_highest_value_year
find_lowest_value_year
create_line_chart
create_multi_line_chart
```

This is the best first example to run.

---

## What This Example Teaches

This example teaches the basic EconKit workflow:

```text
load data
clean data
validate data
summarize data
visualize data
write a report
```

It is useful for students who want to understand how raw economic data becomes readable analysis.

---

## Output Interpretation

The generated Markdown file summarizes:

- dataset size
- year range
- average values
- highest values
- lowest values
- summary statistics
- correlation matrix
- basic interpretation notes

The generated charts show:

- GDP growth over time
- inflation over time
- multiple macro indicators over time

---

# 2. Macro Risk Analysis

Script:

```text
examples/analyze_macro_risk.py
```

Run:

```bash
python examples/analyze_macro_risk.py
```

This example demonstrates EconKit's macro risk analysis.

Generated outputs:

```text
outputs/examples/macro_risk_example.md
outputs/examples/macro_risk_example.json
```

Main EconKit functions used:

```python
load_economic_data
clean_macro_dataset
validate_macro_dataset
analyze_macro_risk
```

---

## What This Example Teaches

This example teaches how EconKit classifies macroeconomic risk using transparent signals.

The analysis includes:

```text
latest year
latest economic values
inflation pressure
growth condition
labor market condition
monetary condition
risk score
overall macro risk
summary text
```

---

## Macro Risk Logic

EconKit builds macro risk from several signals:

| Signal | Input |
|---|---|
| Inflation pressure | `inflation_rate` |
| Growth condition | `gdp_growth` |
| Labor market | `unemployment_rate` |
| Monetary condition | `interest_rate` |

The risk score increases when the economy shows warning signs such as:

- high inflation
- weak growth
- high unemployment
- tight monetary conditions

Possible overall labels:

```text
Low
Moderate
Elevated
High
```

---

## Output Interpretation

The Markdown output explains the result in plain English.

The JSON output is useful for:

- automated workflows
- notebooks
- dashboards
- future apps
- testing
- reproducible analysis

---

# 3. Report Generation

Script:

```text
examples/generate_report.py
```

Run:

```bash
python examples/generate_report.py
```

This example generates professional Markdown reports and charts.

Generated outputs:

```text
outputs/examples/report/economic_report.md
outputs/examples/report/monetary_policy_report.md
outputs/examples/report/data_quality_report.md
outputs/examples/report/gdp_growth.png
outputs/examples/report/inflation_rate.png
outputs/examples/report/unemployment_rate.png
outputs/examples/report/interest_rate.png
outputs/examples/report/macro_indicators.png
outputs/examples/report_index.md
```

Main EconKit functions used:

```python
generate_economic_report
analyze_macro_risk
analyze_monetary_policy_stance
analyze_business_cycle
analyze_inflation_pressure
analyze_policy_mix
```

---

## What This Example Teaches

This example teaches how EconKit moves from a dataset to a complete report package.

It is useful for:

- class projects
- research prototypes
- policy memo drafts
- GitHub portfolio projects
- reproducible analysis demonstrations

---

## Generated Report Types

### `economic_report.md`

The main economic analysis report.

It includes:

- dataset overview
- executive summary
- summary statistics
- indicator highlights
- correlation matrix
- macro risk analysis
- monetary policy stance
- business-cycle diagnosis
- inflation pressure diagnosis

### `monetary_policy_report.md`

A focused monetary policy report.

It includes:

- actual interest rate
- policy-rule benchmark
- policy gap
- real interest rate
- assumptions
- summary interpretation

### `data_quality_report.md`

A dataset quality report.

It includes:

- missing values
- duplicate rows
- year range
- detected issues

### `report_index.md`

A dashboard-like index file summarizing all generated outputs.

---

# 4. Macro Scenario Simulation

Script:

```text
examples/run_macro_scenarios.py
```

Run:

```bash
python examples/run_macro_scenarios.py
```

This example generates and compares macroeconomic scenarios.

Generated outputs:

```text
outputs/examples/scenarios/baseline_scenario.csv
outputs/examples/scenarios/stagflation_scenario.csv
outputs/examples/scenarios/soft_landing_scenario.csv
outputs/examples/scenarios/hard_landing_scenario.csv
outputs/examples/scenarios/supply_recovery_scenario.csv
outputs/examples/scenarios/policy_mistake_scenario.csv
outputs/examples/scenarios/scenario_comparison.csv
outputs/examples/scenarios/macro_scenario_report.md
outputs/examples/scenario_dashboard.md
```

Main EconKit functions used:

```python
build_stress_test_scenarios
compare_macro_scenarios
generate_macro_scenario_analysis
```

---

## What This Example Teaches

This example teaches how to compare possible macroeconomic paths.

It is useful for asking questions like:

- What happens under an inflation shock?
- What happens under a recession shock?
- What does a soft landing look like?
- Which scenario creates the highest macro risk?
- How do stress tests differ from the baseline?

---

## Scenario Types

The stress-test example includes:

| Scenario | Interpretation |
|---|---|
| `baseline` | Continuation of recent macro conditions |
| `stagflation` | Weak growth and high inflation pressure |
| `soft_landing` | Inflation cools while growth remains stable |
| `hard_landing` | Sharp negative demand shock |
| `supply_recovery` | Improved supply conditions lower inflation |
| `policy_mistake` | Weak demand plus excessive tightening |

---

## Scenario Comparison

The comparison file includes:

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

This helps users compare the final-year outcomes across scenarios.

---

# 5. Forecasting

Script:

```text
examples/run_forecasting.py
```

Run:

```bash
python examples/run_forecasting.py
```

This example generates simple macroeconomic forecasts.

Generated outputs:

```text
outputs/examples/forecasts/ar1_forecasts.csv
outputs/examples/forecasts/moving_average_forecasts.csv
outputs/examples/forecasts/forecast_summary.md
```

Main EconKit functions used:

```python
forecast_ar1
forecast_moving_average
generate_forecast_table
```

---

## What This Example Teaches

This example teaches two simple forecasting approaches.

### AR(1) Forecast

An AR(1) forecast uses the previous value of a variable to project future values.

Plain idea:

```text
future value depends partly on the current value
```

### Moving-Average Forecast

A moving-average forecast uses recent average values as a simple baseline.

Plain idea:

```text
future value is close to the recent average
```

---

## Forecasted Indicators

The example forecasts:

```text
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

The generated forecast tables can be opened in Excel, Google Sheets, pandas, or a text editor.

---

## Forecasting Warning

Forecasts from small datasets can be unstable.

EconKit forecasts are designed for:

- learning
- baseline projections
- transparent examples
- exploratory analysis

They are not official forecasts.

---

# 6. Regression

Script:

```text
examples/run_regression.py
```

Run:

```bash
python examples/run_regression.py
```

This example runs lightweight OLS regression.

Generated outputs:

```text
outputs/examples/regression/regression_report.md
outputs/examples/regression/regression_result.json
outputs/examples/regression/regression_summary.md
```

Main EconKit functions used:

```python
run_ols_formula
regression_report
```

---

## What This Example Teaches

This example teaches how to run simple regression models using EconKit.

Example formula:

```python
"inflation_rate ~ gdp_growth + unemployment_rate"
```

This means:

```text
Dependent variable:
inflation_rate

Independent variables:
gdp_growth
unemployment_rate
```

---

## Regression Models Included

The example runs:

```text
inflation_rate ~ gdp_growth + unemployment_rate
gdp_growth ~ inflation_rate + interest_rate
unemployment_rate ~ gdp_growth + interest_rate
```

Each result includes:

```text
coefficients
standard errors
t-statistics
residuals
fitted values
R-squared
adjusted R-squared
number of observations
```

---

## Regression Warning

Regression describes relationships in the data.

Regression does not automatically prove causality.

A causal claim requires a research design.

For example, this is careful:

```text
GDP growth is associated with inflation in this sample.
```

This is too strong:

```text
GDP growth causes inflation.
```

---

# Recommended Learning Order

For beginners, use this order:

```text
1. analyze_macro_data.py
2. analyze_macro_risk.py
3. generate_report.py
4. run_macro_scenarios.py
5. run_forecasting.py
6. run_regression.py
```

Reason:

| Step | Why |
|---|---|
| 1 | Learn basic data loading and summaries |
| 2 | Learn macro risk diagnostics |
| 3 | Learn report generation |
| 4 | Learn scenario simulation |
| 5 | Learn forecasting |
| 6 | Learn regression |

---

# Recommended Project Demonstration

For a professional GitHub demonstration, run:

```bash
python examples/analyze_macro_data.py
python examples/analyze_macro_risk.py
python examples/generate_report.py
python examples/run_macro_scenarios.py
python examples/run_forecasting.py
python examples/run_regression.py
```

Then show that outputs were generated in:

```text
outputs/examples/
```

This demonstrates that EconKit is more than a static code repository.

It shows:

- data analysis
- diagnostics
- reporting
- scenario simulation
- forecasting
- regression
- reproducible outputs

---

# CLI Alternatives

Every example has a CLI alternative.

## Basic report

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

## Risk

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

## Policy

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
```

## Cycle

```bash
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
```

## Inflation

```bash
python src/econkit_cli.py inflation data/sample_economic_data.csv --output-dir outputs/inflation
```

## Scenarios

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5 --stress-tests
```

## Forecast

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv --output-dir outputs/forecasts --periods 5
```

## Regression

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression
```

## Full workflow

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5 --stress-tests
```

---

# Troubleshooting Examples

## Import error

If an example cannot import `econkit`, make sure you run it from the project root:

```bash
python examples/analyze_macro_data.py
```

Do not run it from inside the `examples` folder unless you know how to adjust Python paths.

---

## Dataset not found

If you see:

```text
FileNotFoundError
```

check that this file exists:

```text
data/sample_economic_data.csv
```

---

## Missing required columns

If you see:

```text
Missing required columns
```

check that the dataset contains:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

---

## Markdown table error

If Markdown tables do not render correctly, install:

```bash
pip install tabulate
```

The `requirements.txt` file already includes `tabulate`.

---

## Chart generation error

If chart generation fails, check that `matplotlib` is installed:

```bash
pip install matplotlib
```

The `requirements.txt` file already includes `matplotlib`.

---

# How to Create Your Own Example

A good EconKit example should follow this structure:

```python
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from econkit import load_economic_data, clean_macro_dataset, validate_macro_dataset

DATA_PATH = PROJECT_ROOT / "data" / "sample_economic_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "examples" / "my_example"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_economic_data(DATA_PATH)
    data = clean_macro_dataset(data)
    validate_macro_dataset(data)

    # Your analysis here


if __name__ == "__main__":
    main()
```

Good example scripts should:

- be runnable from the project root
- use the sample dataset
- save outputs under `outputs/examples`
- print clear progress messages
- include educational comments
- avoid hidden dependencies
- avoid private data
- avoid overclaiming results

---

# Educational Disclaimer

The examples are designed for learning and exploratory economic analysis.

They are not:

- official forecasts
- investment advice
- central-bank policy recommendations
- proof of causal relationships
- substitutes for professional econometric software

Use the examples as starting points for economic reasoning and reproducible analysis.
