# EconKit

![Run Tests](https://github.com/car6770/econkit/actions/workflows/tests.yml/badge.svg)

EconKit is an open-source Python toolkit for beginner-friendly economics data analysis.

The goal of this project is to help students and early researchers organize, clean, analyze, visualize, and interpret economic data using Python.

## What is EconKit?

EconKit provides simple examples, reusable Python functions, automated reports, and beginner-friendly interpretation tools for basic economics data analysis.

It is designed for students who are learning how to work with economic datasets and want clear examples that connect economic theory with actual Python workflows.

## Why this project matters

Many economics students study macroeconomic concepts such as inflation, GDP growth, unemployment, and interest rates, but they often lack simple, beginner-friendly tools for analyzing these indicators with real data.

EconKit aims to make economics data analysis easier by providing:

* Small sample datasets
* Clear Python examples
* Reusable analysis functions
* Automated report generation
* Basic macroeconomic interpretation tools
* Beginner-friendly documentation

## Educational purpose

EconKit is designed as an educational open-source project for economics students who are learning Python-based data analysis.

This project helps students practice how to move from raw data to analysis, visualization, interpretation, and written reporting.

The project is especially useful for students who want to learn how to analyze macroeconomic indicators such as:

* GDP growth
* Inflation
* Unemployment
* Interest rates

## Main features

* Load economic datasets from CSV files
* Calculate summary statistics
* Find highest and lowest values by year
* Visualize macroeconomic trends
* Generate Markdown economic analysis reports
* Analyze simple macroeconomic risk conditions
* Use a command-line interface for report generation
* Provide beginner-friendly examples and tutorials

## Project structure

* `data/sample_economic_data.csv`: sample macroeconomic dataset
* `examples/analyze_macro_data.py`: example Python script for analysis and visualization
* `examples/generate_report.py`: example script for generating an economic report
* `examples/analyze_macro_risk.py`: example script for macro risk analysis
* `src/econkit.py`: reusable Python functions for economic data analysis
* `src/econkit_cli.py`: command-line interface for EconKit
* `tests/`: automated tests for core functions and CLI tools
* `docs/tutorial.md`: beginner-friendly tutorial
* `docs/sample_report.md`: sample economic report
* `requirements.txt`: required Python packages

## Installation

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

## Basic usage

Run the basic macroeconomic analysis example:

```bash
python examples/analyze_macro_data.py
```

The example script loads the sample economic dataset, prints summary statistics, and creates simple visualizations for inflation and GDP growth.

## Example dataset

The sample dataset includes basic macroeconomic indicators:

* GDP growth
* Inflation rate
* Unemployment rate
* Interest rate

This dataset is designed for educational practice and beginner-friendly economic data analysis.

## Report generator

EconKit includes a simple report generator for macroeconomic datasets.

The report generator can:

* Load economic data from CSV
* Calculate summary statistics
* Find highest and lowest values by year
* Create line charts for key indicators
* Generate a Markdown economic analysis report

Run the report generator with:

```bash
python examples/generate_report.py
```

Generated reports and charts are saved in the `outputs/` directory.

## Sample output

A sample economic report is available here:

[docs/sample_report.md](docs/sample_report.md)

## Macro Risk Analyzer

EconKit includes a simple macroeconomic risk analyzer.

The macro risk analyzer uses the latest observation in a dataset to classify basic macroeconomic conditions, including:

* Inflation pressure
* GDP growth condition
* Labor market condition
* Monetary condition
* Overall macroeconomic risk level

Run the macro risk analysis example with:

```bash
python examples/analyze_macro_risk.py
```

The analyzer produces a beginner-friendly summary that helps students connect macroeconomic indicators with basic economic interpretation.

This feature is designed for educational use. It is not intended to be a formal forecast or professional economic assessment.

## Command-line interface

EconKit includes a simple command-line interface for generating economic analysis outputs from a CSV dataset.

You can run the CLI with:

```bash
python src/econkit_cli.py data/sample_economic_data.csv --output-dir outputs
```

The CLI will generate:

* A Markdown economic analysis report
* Line charts for macroeconomic indicators
* A macro risk summary
* Beginner-friendly interpretation of the latest economic conditions

Generated files are saved in the `outputs/` directory.

This makes EconKit usable as a small command-line tool for economics students learning Python-based data analysis.

## Testing

EconKit includes automated tests for core functions and command-line tools.

Run tests with:

```bash
pytest
```

The project also uses GitHub Actions to run tests automatically when changes are pushed.

## Tutorial

A beginner-friendly tutorial is available here:

[docs/tutorial.md](docs/tutorial.md)

## Example use cases

EconKit can be used for:

* Inflation trend analysis
* Interest rate comparison
* GDP growth visualization
* Unemployment rate analysis
* Basic macroeconomic time-series practice
* Beginner-friendly economic report generation
* Simple macroeconomic risk interpretation

## Maintenance plan

This repository will be maintained through regular updates, including:

* Adding new economics datasets
* Improving beginner-friendly tutorials
* Adding tests for core functions
* Expanding documentation
* Reviewing issues and planned improvements
* Creating small releases as the project grows

## Project status

EconKit is in early development.

The current version includes sample data, analysis examples, automated report generation, macro risk analysis, CLI support, tests, documentation, and releases.

Planned improvements include:

* More sample economic datasets
* More beginner-friendly tutorials
* Additional visualization examples
* More tests for edge cases
* Expanded documentation for economics students
* More practical examples connecting economic theory with Python analysis

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
