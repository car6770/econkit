# EconKit Troubleshooting Guide

This guide explains common problems users may encounter when installing, testing, running, or extending EconKit.

The goal is to make errors easier to understand and fix.

---

## Quick Checklist

Before debugging deeply, check these first:

```bash
python --version
pip --version
pip install -r requirements.txt
pytest
```

Then validate the sample dataset:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

If that passes, the basic project setup is working.

---

# 1. Installation Problems

## Problem: `pip install -r requirements.txt` fails

### Possible causes

- Python version is too old
- pip is outdated
- internet connection issue
- dependency conflict

### Fix

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then reinstall:

```bash
pip install -r requirements.txt
```

If you are using a virtual environment, activate it first.

---

## Problem: `python` command not found

Some systems use `python3` instead of `python`.

Try:

```bash
python3 --version
```

Then use:

```bash
python3 -m pip install -r requirements.txt
python3 src/econkit_cli.py features
```

---

## Problem: package installs but import fails

Example error:

```text
ModuleNotFoundError: No module named 'econkit'
```

### Fix 1: Run from the project root

Make sure your current folder is the repository root:

```text
econkit/
  src/
  tests/
  data/
  examples/
```

Then run:

```bash
python src/econkit_cli.py features
```

### Fix 2: Install editable package

```bash
pip install -e .
```

Then test:

```bash
python -c "import econkit; print('ok')"
```

---

# 2. GitHub Actions Problems

## Problem: GitHub Actions is red

Click the failed workflow:

```text
GitHub repository → Actions → Run Tests → failed run
```

Then open the failed step.

Common failed steps:

```text
Install dependencies
Syntax check
Run pytest
CLI smoke tests
```

---

## Problem: dependency installation failed in Actions

Check that `requirements.txt` exists in the repository root.

Expected location:

```text
requirements.txt
```

Then check that it includes:

```text
numpy
pandas
matplotlib
tabulate
pytest
```

---

## Problem: syntax check failed

The workflow checks:

```bash
python -m py_compile src/econkit.py
python -m py_compile src/econkit_cli.py
```

If this fails, there is likely a Python syntax error.

Common causes:

- missing comma
- missing closing parenthesis
- incorrect indentation
- unclosed string
- copied text into the wrong file

Fix the exact line shown in the error.

---

## Problem: pytest failed

Run locally if possible:

```bash
pytest
```

If you cannot run locally, read the Actions error carefully.

Common causes:

- function name mismatch
- expected dictionary key missing
- file uploaded to the wrong path
- test file accidentally uploaded into `src/`
- old version of a file still in the repository

---

## Problem: CLI smoke test failed

The workflow may run:

```bash
python src/econkit_cli.py features
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Check that these files exist:

```text
src/econkit_cli.py
data/sample_economic_data.csv
```

Also check that the sample dataset has the required columns:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

---

# 3. Dataset Problems

## Problem: missing required columns

Example error:

```text
Missing required columns: inflation_rate
```

### Fix

Make sure your dataset has these exact columns:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

Column names are case-sensitive after cleaning.

Recommended CSV header:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
```

---

## Problem: wrong column names

Examples of problematic names:

```text
GDP
GDP Growth Rate
Inflation
Unemployment
Interest
```

EconKit expects:

```text
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

Rename columns before analysis, or use `clean_column_names` if the names are close enough.

---

## Problem: missing values

Example:

```text
Column 'inflation_rate' contains missing values.
```

### Fix

Open the CSV file and check for empty cells.

Example bad row:

```csv
2023,1.4,,2.7,3.50
```

Example fixed row:

```csv
2023,1.4,3.6,2.7,3.50
```

---

## Problem: duplicate years

Example:

```text
Year column contains duplicate years.
```

### Fix

Make sure each year appears once.

Bad:

```csv
2024,2.0,2.3,2.8,3.5
2024,2.1,2.4,2.7,3.6
```

Good:

```csv
2024,2.0,2.3,2.8,3.5
```

---

## Problem: year is not numeric

Bad:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
twenty twenty four,2.0,2.3,2.8,3.5
```

Good:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
2024,2.0,2.3,2.8,3.5
```

---

# 4. CLI Problems

## Problem: command not recognized

Example:

```text
invalid choice: 'risks'
```

### Fix

Use the exact command name.

Correct:

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv
```

Incorrect:

```bash
python src/econkit_cli.py risks data/sample_economic_data.csv
```

---

## Problem: required argument missing

Example:

```text
the following arguments are required: data_path
```

### Fix

Most commands need a dataset path.

Example:

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

---

## Problem: output folder does not exist

EconKit usually creates output folders automatically.

However, if your system blocks file creation, create the folder manually:

```bash
mkdir -p outputs
```

Then rerun the command.

---

## Problem: Markdown tables are not generated

If pandas cannot create Markdown tables, install `tabulate`:

```bash
pip install tabulate
```

The dependency should already be included in `requirements.txt`.

---

# 5. Example Script Problems

## Problem: example cannot import EconKit

Run examples from the project root.

Correct:

```bash
python examples/analyze_macro_data.py
```

Incorrect:

```bash
cd examples
python analyze_macro_data.py
```

The examples assume this structure:

```text
PROJECT_ROOT/
  src/
  examples/
  data/
```

---

## Problem: example cannot find sample data

Check that this file exists:

```text
data/sample_economic_data.csv
```

If it does not exist, add the sample dataset again.

---

## Problem: examples generate many files

That is normal.

Examples write outputs to:

```text
outputs/examples/
```

The `outputs/` folder is ignored by Git so generated files do not clutter the repository.

---

# 6. Chart Problems

## Problem: chart file is not created

Check that `matplotlib` is installed:

```bash
pip install matplotlib
```

Then rerun the example.

---

## Problem: chart looks empty

Possible causes:

- selected column has missing values
- selected column is not numeric
- dataset has only one row
- wrong column name was passed

Check:

```python
print(data.head())
print(data.dtypes)
```

---

## Problem: chart cannot be shown on server

EconKit saves charts to files.

It does not need to open an interactive chart window.

Look for files like:

```text
outputs/examples/gdp_growth_chart.png
```

---

# 7. Regression Problems

## Problem: formula is invalid

Correct formula:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

Incorrect formulas:

```text
inflation_rate = gdp_growth + unemployment_rate
inflation_rate gdp_growth unemployment_rate
inflation_rate ~
```

Use:

```python
run_ols_formula(data, "inflation_rate ~ gdp_growth + unemployment_rate")
```

---

## Problem: regression variable not found

Example error:

```text
Column not found: gdp
```

### Fix

Use exact column names from the dataset.

Check:

```python
print(data.columns)
```

---

## Problem: regression has too few observations

OLS needs enough observations relative to the number of variables.

If your dataset is very small, reduce the number of independent variables.

Bad for tiny data:

```text
y ~ x1 + x2 + x3 + x4 + x5
```

Better:

```text
y ~ x1 + x2
```

---

## Problem: regression result is interpreted too strongly

Regression does not automatically prove causality.

Careful wording:

```text
GDP growth is associated with inflation in this sample.
```

Too strong:

```text
GDP growth causes inflation.
```

---

# 8. Forecasting Problems

## Problem: AR(1) forecast fails

Possible causes:

- too few observations
- non-numeric column
- missing values

Check:

```python
data["gdp_growth"].dropna()
```

If the dataset is too small, use moving average instead.

---

## Problem: forecast looks unrealistic

Simple forecasts are baseline projections.

They do not know about:

- wars
- pandemics
- financial crises
- policy regime changes
- structural breaks
- new government policies
- global commodity shocks

Use forecasts as learning tools, not official predictions.

---

# 9. Scenario Problems

## Problem: scenario output seems too simple

That is intentional.

EconKit scenarios are transparent teaching simulations.

They are not structural macroeconomic models.

The purpose is to compare paths under different assumptions.

---

## Problem: scenario values become negative

Some variables are bounded internally, but users should still inspect outputs.

If a scenario is too extreme, reduce the shock size.

Example:

```python
simulate_macro_scenario(data, "mild_recession", demand_shock=-1.0)
```

instead of:

```python
simulate_macro_scenario(data, "severe_recession", demand_shock=-5.0)
```

---

# 10. Common GitHub Upload Mistakes

## Mistake: uploading a file to the wrong folder

Correct examples:

```text
src/econkit.py
src/econkit_cli.py
tests/test_econkit.py
tests/test_cli.py
data/sample_economic_data.csv
docs/api.md
examples/run_forecasting.py
```

If a file goes to the wrong folder, GitHub Actions may fail.

---

## Mistake: renaming files accidentally

GitHub or your browser may rename downloaded files like:

```text
econkit (1).py
test_econkit copy.py
```

Do not upload renamed files.

Use the exact expected file name.

---

## Mistake: uploading zip file instead of extracted files

If a pack is provided as a zip file, unzip it first.

Upload the files inside the zip, not the zip itself, unless the instructions say otherwise.

---

## Mistake: hidden files are not visible

Files starting with a dot may be hidden on Mac or Linux.

Examples:

```text
.github/
.gitignore
```

If they are not visible, create them manually in GitHub using:

```text
Add file → Create new file
```

Then type the full path.

Example:

```text
.github/workflows/tests.yml
```

---

# 11. When to Open an Issue

Open a bug report if:

- the sample dataset fails validation
- examples do not run
- CLI commands fail with valid input
- documentation command examples are wrong
- GitHub Actions fails on a clean repository
- an error message is confusing

Use:

```text
.github/ISSUE_TEMPLATE/bug_report.md
```

---

# 12. Good Debugging Habits

When debugging EconKit, write down:

```text
What command did I run?
What file did I use?
What error message appeared?
What did I expect?
What actually happened?
```

This makes it much easier to fix problems.

---

# 13. Minimal Working Check

If everything seems broken, try this minimal sequence:

```bash
pip install -r requirements.txt
python src/econkit_cli.py features
python src/econkit_cli.py validate data/sample_economic_data.csv
pytest
```

If all four pass, the core project is working.

---

# Summary

Most EconKit problems come from:

```text
wrong file path
wrong file name
missing dependency
wrong dataset columns
running commands from the wrong folder
copying a file into the wrong GitHub location
```

Start with the quick checklist, then inspect the exact error message.
