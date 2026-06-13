# EconKit

![Run Tests](https://github.com/car6770/econkit/actions/workflows/tests.yml/badge.svg)

EconKit is an open-source Python toolkit for beginner-friendly economics data analysis, automated reporting, macroeconomic risk analysis, and macroeconomic scenario simulation.

The goal of this project is to help economics students and early researchers move from raw macroeconomic data to summary statistics, visualizations, written reports, risk interpretation, and scenario analysis using Python.

## What is EconKit?

EconKit provides reusable Python functions, command-line tools, examples, tests, and documentation for basic economics data analysis.

It is designed for students who are learning how to work with economic datasets and want clear, practical examples that connect economic concepts with Python workflows.

## Why this project matters

Many economics students study concepts such as inflation, GDP growth, unemployment, interest rates, and macroeconomic shocks, but they often lack simple tools for practicing these ideas with data.

EconKit aims to make macroeconomic data analysis easier by providing:

* Small sample datasets
* Clear Python examples
* Automated Markdown reports
* Simple visualizations
* Macro risk classification
* Scenario simulation tools
* Beginner-friendly documentation
* A command-line interface

## Main features

* Validate economic CSV datasets
* Load and clean macroeconomic data
* Calculate summary statistics
* Find highest and lowest values by year
* Create line charts for macroeconomic indicators
* Generate Markdown economic analysis reports
* Analyze macroeconomic risk using simple educational thresholds
* Simulate macroeconomic scenarios
* Compare baseline, inflation shock, recession shock, and tight policy scenarios
* Run the full workflow from the command line
* Run automated tests with GitHub Actions

## Project structure

* `data/sample_economic_data.csv`: sample macroeconomic dataset
* `src/econkit.py`: core EconKit functions
* `src/econkit_cli.py`: command-line interface
* `examples/analyze_macro_data.py`: basic analysis example
* `examples/generate_report.py`: report generation example
* `examples/analyze_macro_risk.py`: macro risk analysis example
* `examples/run_macro_scenarios.py`: macro scenario simulation example
* `tests/`: automated tests
* `docs/tutorial.md`: beginner tutorial
* `docs/cli.md`: CLI guide
* `docs/sample_report.md`: sample report
* `pyproject.toml`: Python project configuration
* `requirements.txt`: required packages

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

For development, install the package in editable mode:

```bash
pip install -e .
```

## Quick start

Run the full EconKit analysis pipeline:

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

This command generates:

* Economic report
* Line charts
* Macro risk summary
* Macro risk JSON output
* Scenario simulation files
* Scenario comparison report

If installed as a package, EconKit can also be run with:

```bash
econkit all data/sample_economic_data.csv --output-dir outputs --years 5
```

## Command-line interface

EconKit includes a CLI with several commands.

### Validate dataset

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

### Generate report

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

### Analyze macro risk

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

### Run macro scenarios

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

### Run full pipeline

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

A full CLI guide is available here:

[docs/cli.md](docs/cli.md)

## Required dataset format

Input CSV files should include the following columns:

* `year`
* `gdp_growth`
* `inflation_rate`
* `unemployment_rate`
* `interest_rate`

The sample dataset is available here:

`data/sample_economic_data.csv`

## Report generator

EconKit can generate a Markdown economic analysis report from a macroeconomic dataset.

The report generator can:

* Load economic data from CSV
* Calculate summary statistics
* Find highest and lowest values by year
* Create charts for key indicators
* Generate a written Markdown report

Run the report example:

```bash
python examples/generate_report.py
```

A sample report is available here:

[docs/sample_report.md](docs/sample_report.md)

## Macro Risk Analyzer

EconKit includes a simple macroeconomic risk analyzer.

The analyzer uses the latest observation in a dataset to classify:

* Inflation pressure
* GDP growth condition
* Labor market condition
* Monetary condition
* Overall macroeconomic risk level

Run the macro risk example:

```bash
python examples/analyze_macro_risk.py
```

This feature helps students connect macroeconomic indicators with basic interpretation rules.

Educational note: this tool is not intended to be a formal forecast or professional economic assessment.

## Macro Scenario Simulator

EconKit includes a simple macroeconomic scenario simulator.

The simulator can generate and compare:

* Baseline scenario
* Inflation shock scenario
* Recession shock scenario
* Tight monetary policy scenario

Run the scenario example:

```bash
python examples/run_macro_scenarios.py
```

The scenario simulator generates:

* Scenario CSV files
* Scenario comparison table
* Markdown scenario analysis report

This feature helps students understand how different macroeconomic shocks may affect GDP growth, inflation, unemployment, interest rates, and overall macro risk.

Educational note: the scenario simulator uses simple educational rules and is not intended to be a professional forecasting model.

## Testing

Run tests with:

```bash
pytest
```

The project also uses GitHub Actions to run tests automatically when changes are pushed.

## Documentation

* [Beginner tutorial](docs/tutorial.md)
* [CLI guide](docs/cli.md)
* [Sample economic report](docs/sample_report.md)

## Example use cases

EconKit can be used for:

* Inflation trend analysis
* GDP growth visualization
* Unemployment rate analysis
* Interest rate comparison
* Beginner-friendly economic reporting
* Simple macro risk interpretation
* Macroeconomic scenario comparison
* Teaching Python-based economics data analysis

## Project status

EconKit is in early development, but the project now includes a complete beginner-friendly workflow:

1. Dataset validation
2. Summary statistics
3. Visualization
4. Report generation
5. Macro risk analysis
6. Scenario simulation
7. CLI workflow
8. Automated testing

Planned improvements include:

* More sample economic datasets
* More tutorials for economics students
* Additional visualization tools
* More robust validation
* Expanded scenario assumptions
* More examples connecting economic theory with Python analysis

## Contributing

Contributions are welcome.

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Code of Conduct

This project follows a simple code of conduct to keep the community respectful and beginner-friendly.

Please read the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file before participating in discussions or contributions.

## Maintainer

This project is maintained by Gyujin Lee.

## License

This project is licensed under the MIT License.
