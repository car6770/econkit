# EconKit CLI Guide

EconKit includes a command-line interface for beginner-friendly economics data analysis.

The CLI allows users to validate datasets, generate reports, analyze macroeconomic risk, simulate macroeconomic scenarios, and run the full analysis pipeline.

## Required dataset format

The input CSV file should include the following columns:

* `year`
* `gdp_growth`
* `inflation_rate`
* `unemployment_rate`
* `interest_rate`

The sample dataset is available at:

`data/sample_economic_data.csv`

## Validate a dataset

Use the `validate` command to check whether a dataset has the required columns.

Command:

`python src/econkit_cli.py validate data/sample_economic_data.csv`

This command checks that the dataset includes all required macroeconomic indicators.

## Generate an economic report

Use the `report` command to generate a Markdown report and charts.

Command:

`python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report`

This command generates:

* A Markdown economic analysis report
* Line charts for macroeconomic indicators

## Analyze macroeconomic risk

Use the `risk` command to classify the latest macroeconomic conditions.

Command:

`python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk`

This command generates:

* A Markdown macro risk summary
* A JSON macro risk summary
* A beginner-friendly interpretation of macroeconomic conditions

## Run macroeconomic scenarios

Use the `scenarios` command to simulate future macroeconomic scenarios.

Command:

`python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5`

This command generates:

* Baseline scenario
* Inflation shock scenario
* Recession shock scenario
* Tight monetary policy scenario
* Scenario comparison table
* Markdown scenario analysis report

## Run the full pipeline

Use the `all` command to run the full EconKit workflow.

Command:

`python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5`

This command generates:

* Economic report
* Charts
* Macro risk summary
* Macro risk JSON output
* Scenario simulation files
* Scenario comparison report

## Installed command usage

If EconKit is installed as a Python package, users can run:

`econkit all data/sample_economic_data.csv --output-dir outputs`

This is supported by the project configuration in `pyproject.toml`.

## Educational note

EconKit is designed for educational use.

The CLI helps economics students practice moving from raw macroeconomic data to summary statistics, visualizations, risk interpretation, and scenario analysis.

The macro risk and scenario tools use simple educational rules and are not intended to be professional forecasts or official economic assessments.
