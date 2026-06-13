# EconKit CLI Guide

EconKit includes a command-line interface for beginner-friendly economics data analysis.

The CLI allows users to:

- Validate economic datasets
- Generate Markdown reports and charts
- Analyze macroeconomic risk
- Analyze monetary policy stance
- Simulate macroeconomic scenarios
- Run the full analysis pipeline

---

## Required dataset format

The input CSV file should include the following columns:

- `year`
- `gdp_growth`
- `inflation_rate`
- `unemployment_rate`
- `interest_rate`

The sample dataset is available at:

```bash
data/sample_economic_data.csv
```

---

## Validate a dataset

Use the `validate` command to check whether a dataset has the required columns.

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

This command checks that the dataset includes all required macroeconomic indicators.

---

## Generate an economic report

Use the `report` command to generate a Markdown report and charts.

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

This command generates:

- A Markdown economic analysis report
- Line charts for macroeconomic indicators
- A monetary policy stance section inside the report

---

## Analyze macroeconomic risk

Use the `risk` command to classify the latest macroeconomic conditions.

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

This command generates:

- A Markdown macro risk summary
- A JSON macro risk summary
- A beginner-friendly interpretation of macroeconomic conditions

The macro risk analyzer classifies:

- Inflation pressure
- Growth condition
- Labor market condition
- Monetary condition
- Overall macroeconomic risk

---

## Analyze monetary policy stance

Use the `policy` command to analyze whether monetary policy looks tight, neutral, or accommodative.

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
```

This command generates:

- A Markdown monetary policy summary
- A JSON monetary policy summary
- A beginner-friendly interpretation of the policy stance

The monetary policy analyzer compares:

- The actual interest rate
- A simple policy-rule benchmark rate
- The gap between the actual rate and the benchmark rate

The policy stance can be classified as:

- `Tight`
- `Moderately Tight`
- `Neutral`
- `Moderately Accommodative`
- `Accommodative`

---

## Customize monetary policy assumptions

Users can also customize the assumptions used in the simple policy rule.

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv \
  --output-dir outputs/policy \
  --target-inflation 2.0 \
  --neutral-interest-rate 2.5 \
  --potential-growth 2.0
```

Available options:

- `--target-inflation`: inflation target used in the policy rule
- `--neutral-interest-rate`: neutral interest rate used in the policy rule
- `--potential-growth`: potential growth rate used in the policy rule

If `neutral-interest-rate` or `potential-growth` is not provided, EconKit estimates them from recent historical data.

---

## Run macroeconomic scenarios

Use the `scenarios` command to simulate future macroeconomic scenarios.

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

This command generates:

- Baseline scenario
- Inflation shock scenario
- Recession shock scenario
- Tight monetary policy scenario
- Scenario CSV files
- Scenario comparison table
- Markdown scenario analysis report

---

## Run the full pipeline

Use the `all` command to run the full EconKit workflow.

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

This command generates:

- Economic report
- Line charts
- Macro risk Markdown summary
- Macro risk JSON output
- Monetary policy Markdown summary
- Monetary policy JSON output
- Scenario simulation files
- Scenario comparison report

---

## Installed command usage

If EconKit is installed as a Python package, users can run:

```bash
econkit all data/sample_economic_data.csv --output-dir outputs --years 5
```

For monetary policy analysis, users can run:

```bash
econkit policy data/sample_economic_data.csv --output-dir outputs/policy
```

This is supported by the project configuration in `pyproject.toml`.

---

## Example workflow

A beginner can run the following workflow:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

Or run everything at once:

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

---

## Educational note

EconKit is designed for educational use.

The CLI helps economics students practice moving from raw macroeconomic data to:

- Summary statistics
- Visualizations
- Written reports
- Macro risk interpretation
- Monetary policy interpretation
- Scenario analysis

The macro risk, monetary policy, and scenario tools use simple educational rules.

They are not intended to be professional forecasts, official policy recommendations, or formal economic assessments.
