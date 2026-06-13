# EconKit Architecture

This document explains how the EconKit repository is organized and how the main components work together.

EconKit is intentionally designed as a simple but professional Python project.

The goal is to make the codebase easy to understand, easy to test, and easy to extend.

---

## High-Level Structure

```text
econkit/
  src/
    econkit.py
    econkit_cli.py

  tests/
    test_econkit.py
    test_cli.py

  data/
    sample_economic_data.csv
    README.md

  examples/
    analyze_macro_data.py
    analyze_macro_risk.py
    generate_report.py
    run_macro_scenarios.py
    run_forecasting.py
    run_regression.py
    README.md

  docs/
    api.md
    cli.md
    examples.md
    methodology.md
    faq.md
    project_vision.md
    release_checklist.md

  .github/
    workflows/
      tests.yml
    ISSUE_TEMPLATE/
      bug_report.md
      feature_request.md
    pull_request_template.md

  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  SECURITY.md
  LICENSE
  pyproject.toml
  requirements.txt
```

---

# Core Design

EconKit has two main Python files:

```text
src/econkit.py
src/econkit_cli.py
```

## `src/econkit.py`

This is the core library.

It contains the Python functions users import directly.

Examples:

```python
from econkit import load_economic_data
from econkit import analyze_macro_risk
from econkit import run_ols_formula
```

The core file is responsible for:

- loading datasets
- cleaning datasets
- validating datasets
- calculating statistics
- creating charts
- diagnosing macroeconomic conditions
- generating reports
- simulating scenarios
- generating forecasts
- running lightweight regression

---

## `src/econkit_cli.py`

This is the command-line interface.

It allows users to run EconKit from the terminal.

Example:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

The CLI is intentionally thin.

That means the CLI should not contain most of the economic logic.

Instead, the CLI should call functions from `econkit.py`.

This keeps the project easier to maintain.

---

# Data Flow

A typical EconKit workflow follows this sequence:

```text
CSV file
  ↓
load_economic_data
  ↓
clean_macro_dataset
  ↓
validate_macro_dataset
  ↓
analysis functions
  ↓
reports / charts / CSV / JSON outputs
```

Example:

```python
from econkit import (
    load_economic_data,
    clean_macro_dataset,
    validate_macro_dataset,
    analyze_macro_risk,
)

data = load_economic_data("data/sample_economic_data.csv")
data = clean_macro_dataset(data)
validate_macro_dataset(data)

risk = analyze_macro_risk(data)
```

---

# Functional Layers

EconKit can be understood as several layers.

## 1. Input Layer

Responsible for reading and saving files.

Main functions:

```text
load_economic_data
save_dataset
```

Purpose:

- read CSV, Excel, Parquet, or JSON files
- save output datasets
- provide clear error messages

---

## 2. Cleaning Layer

Responsible for making messy data usable.

Main functions:

```text
clean_column_names
coerce_numeric_columns
clean_macro_dataset
```

Purpose:

- standardize column names
- convert values to numeric form
- sort observations by year
- remove duplicate years

---

## 3. Validation Layer

Responsible for catching bad inputs early.

Main functions:

```text
validate_macro_dataset
profile_dataset
data_quality_report
```

Purpose:

- check required columns
- detect missing values
- detect duplicate years
- summarize dataset quality
- prevent confusing downstream errors

---

## 4. Statistics Layer

Responsible for basic quantitative summaries.

Main functions:

```text
calculate_summary_statistics
calculate_average_growth
find_highest_value_year
find_lowest_value_year
calculate_correlation_matrix
calculate_rolling_statistics
calculate_growth_rates
calculate_z_scores
```

Purpose:

- summarize economic indicators
- find high and low years
- calculate correlations
- prepare data for interpretation

---

## 5. Visualization Layer

Responsible for chart generation.

Main functions:

```text
create_line_chart
create_multi_line_chart
create_scatter_chart
```

Purpose:

- create readable charts
- save outputs as image files
- support reports and examples

---

## 6. Macro Diagnostics Layer

Responsible for economic interpretation.

Main functions:

```text
analyze_macro_risk
analyze_monetary_policy_stance
analyze_business_cycle
analyze_inflation_pressure
analyze_policy_mix
```

Purpose:

- classify macro risk
- evaluate policy stance
- diagnose business-cycle conditions
- evaluate inflation pressure
- summarize the overall macro regime

This layer is rule-based and transparent.

---

## 7. Scenario Layer

Responsible for generating possible future macro paths.

Main functions:

```text
simulate_macro_scenario
build_default_macro_scenarios
build_stress_test_scenarios
compare_macro_scenarios
generate_macro_scenario_report
generate_macro_scenario_analysis
```

Purpose:

- simulate baseline and stress scenarios
- compare final-year outcomes
- generate scenario CSV files
- generate scenario reports

---

## 8. Forecasting Layer

Responsible for simple baseline forecasts.

Main functions:

```text
forecast_ar1
forecast_moving_average
generate_forecast_table
```

Purpose:

- generate AR(1) forecasts
- generate moving-average forecasts
- produce forecast tables for reports and examples

---

## 9. Econometrics Layer

Responsible for lightweight regression.

Main functions:

```text
parse_formula
run_ols
run_ols_formula
regression_report
```

Purpose:

- parse simple formulas
- run ordinary least squares
- calculate coefficients and standard errors
- generate regression reports

---

## 10. Reporting Layer

Responsible for turning analysis into readable files.

Main functions:

```text
generate_markdown_report
generate_monetary_policy_report
generate_economic_report
generate_full_analysis_package
```

Purpose:

- create Markdown reports
- create charts
- create full output folders
- support reproducible project demonstrations

---

# CLI Architecture

The CLI exposes EconKit functionality through commands.

Common commands:

```text
validate
profile
report
risk
policy
cycle
inflation
mix
scenarios
forecast
ols
package
features
all
```

Example:

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

The CLI flow is usually:

```text
parse command-line arguments
  ↓
load data
  ↓
call core EconKit function
  ↓
save output
  ↓
print readable status message
```

---

# Testing Architecture

Tests are stored in:

```text
tests/
```

Main test files:

```text
tests/test_econkit.py
tests/test_cli.py
```

The tests check:

- core functions
- macro diagnostics
- scenario simulation
- CLI behavior
- backward compatibility
- expected output structure

Tests are run with:

```bash
pytest
```

GitHub Actions runs the tests automatically on commits and pull requests.

---

# GitHub Actions

Workflow file:

```text
.github/workflows/tests.yml
```

The workflow checks:

- Python installation
- dependency installation
- package installation
- syntax of core files
- pytest test suite
- CLI smoke tests

This helps make the repository look professional and prevents accidental breakage.

---

# Documentation Architecture

Documentation is stored in:

```text
docs/
```

Important docs:

| File | Purpose |
|---|---|
| `api.md` | Python API reference |
| `cli.md` | CLI command guide |
| `examples.md` | Example script guide |
| `methodology.md` | Explanation of analysis logic |
| `faq.md` | Common questions |
| `project_vision.md` | Project purpose and direction |
| `release_checklist.md` | Release preparation checklist |

The README is the front page.

The `docs/` folder provides deeper detail.

---

# Examples Architecture

Examples are stored in:

```text
examples/
```

The examples demonstrate real workflows.

They are not tests, but they should be runnable.

Examples use:

```text
data/sample_economic_data.csv
```

and save outputs to:

```text
outputs/examples/
```

This keeps generated files separate from source code.

---

# Output Architecture

Generated outputs should usually go into:

```text
outputs/
```

Examples:

```text
outputs/examples/
outputs/report/
outputs/scenarios/
outputs/forecasts/
outputs/regression/
```

These files are usually not committed to Git.

Reason:

- generated outputs can become large
- they change often
- they can clutter the repository
- users can regenerate them anytime

The `.gitignore` file excludes generated outputs.

---

# Extension Guidelines

When adding a new feature, follow this pattern.

## 1. Add the Core Function

Add the main logic to:

```text
src/econkit.py
```

The function should:

- have a clear name
- accept explicit arguments
- return a useful object
- raise clear errors
- avoid hidden side effects

---

## 2. Add Tests

Add tests to:

```text
tests/test_econkit.py
```

Good tests should check:

- normal case
- edge case
- expected output keys
- expected output types
- error handling where useful

---

## 3. Add CLI Support if Useful

If the feature is useful from the command line, update:

```text
src/econkit_cli.py
```

The CLI should call the core function.

Avoid duplicating core logic in the CLI.

---

## 4. Add Documentation

Update one or more:

```text
README.md
docs/api.md
docs/cli.md
docs/examples.md
docs/methodology.md
```

---

## 5. Add an Example if Useful

If the feature is important, add an example to:

```text
examples/
```

---

## 6. Update the Changelog

Update:

```text
CHANGELOG.md
```

Explain what changed.

---

# Backward Compatibility

EconKit should avoid breaking existing users.

When changing a function:

- preserve existing argument names when possible
- preserve existing return keys when possible
- add new keys instead of replacing old keys
- keep old aliases when reasonable
- update tests when compatibility matters

Example:

```text
phase
business_cycle_phase
```

Both keys may be supported so older code does not break.

---

# Error Handling Principles

Good EconKit errors should be:

- clear
- actionable
- beginner-friendly

Bad:

```text
KeyError: x
```

Better:

```text
Missing required columns: inflation_rate
```

Bad:

```text
ValueError
```

Better:

```text
Dataset is empty after cleaning. Check the input file.
```

---

# Naming Principles

Function names should be descriptive.

Good:

```text
analyze_macro_risk
generate_forecast_table
calculate_correlation_matrix
```

Less good:

```text
do_analysis
process
run
```

Column names should use snake case:

```text
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

Output files should be descriptive:

```text
macro_risk_summary.md
scenario_comparison.csv
forecast_summary.md
```

---

# Dependency Philosophy

EconKit keeps dependencies simple.

Core dependencies:

```text
pandas
numpy
matplotlib
tabulate
```

Testing dependency:

```text
pytest
```

Why keep dependencies small?

- easier installation
- fewer version conflicts
- better for beginners
- simpler GitHub Actions
- easier maintenance

---

# Security and Privacy Architecture

EconKit should not require private credentials.

The project should avoid:

- API keys in source code
- private datasets in the repository
- secrets in examples
- hidden network calls
- unsafe file operations

Users should be able to run EconKit locally with sample data.

---

# Summary

EconKit architecture is built around this idea:

```text
simple core library
thin CLI
clear tests
runnable examples
deep documentation
reproducible outputs
```

This structure makes the project understandable for beginners and credible as a professional open-source repository.
