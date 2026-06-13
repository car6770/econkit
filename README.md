# EconKit Documentation

Welcome to the EconKit documentation hub.

EconKit is a beginner-friendly but professional Python toolkit for economics data analysis.

This folder contains detailed guides for using, understanding, extending, and maintaining the project.

---

## Start Here

If you are new to EconKit, read these in order:

| Step | Document | Purpose |
|---|---|---|
| 1 | [Project Vision](project_vision.md) | Understand what EconKit is trying to become |
| 2 | [Examples Guide](examples.md) | Learn by running example scripts |
| 3 | [CLI Guide](cli.md) | Use EconKit from the command line |
| 4 | [API Reference](api.md) | Use EconKit from Python |
| 5 | [Methodology](methodology.md) | Understand how the analysis works |

---

## Main Documentation

### [API Reference](api.md)

The Python API reference.

Use this when you want to import EconKit functions directly in Python.

Covers:

- data loading
- data cleaning
- validation
- statistics
- charts
- macro diagnostics
- monetary policy analysis
- business-cycle analysis
- inflation pressure
- policy mix
- scenario simulation
- forecasting
- OLS regression
- report generation

---

### [CLI Guide](cli.md)

The command-line interface guide.

Use this when you want to run EconKit from the terminal.

Example:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Covers:

- validate
- profile
- report
- risk
- policy
- cycle
- inflation
- mix
- scenarios
- forecast
- ols
- package
- features
- all

---

### [Examples Guide](examples.md)

The example script guide.

Use this when you want to learn by running complete workflows.

Example scripts:

```text
examples/analyze_macro_data.py
examples/analyze_macro_risk.py
examples/generate_report.py
examples/run_macro_scenarios.py
examples/run_forecasting.py
examples/run_regression.py
```

---

### [Methodology](methodology.md)

The methodology document explains how EconKit's analysis logic works.

Covers:

- macro risk scoring
- inflation pressure classification
- growth condition classification
- labor-market classification
- monetary condition classification
- policy-rule benchmark
- business-cycle classification
- inflation momentum
- policy mix
- scenario simulation
- forecasting
- OLS regression

---

### [Architecture](architecture.md)

The architecture guide explains the project structure.

Covers:

- repository layout
- core library design
- CLI design
- testing structure
- documentation structure
- examples structure
- output structure
- extension guidelines
- backward compatibility
- dependency philosophy

---

### [Troubleshooting](troubleshooting.md)

The troubleshooting guide explains how to fix common problems.

Covers:

- installation errors
- GitHub Actions failures
- dataset formatting problems
- CLI errors
- example script errors
- chart errors
- regression errors
- forecasting errors
- scenario errors
- GitHub upload mistakes
- hidden file issues

---

### [Glossary](glossary.md)

The glossary explains economics and data-analysis terms in beginner-friendly language.

Covers:

- GDP growth
- inflation
- unemployment
- interest rates
- macro risk
- monetary policy stance
- policy gap
- business cycle
- scenario simulation
- AR(1)
- moving average
- OLS
- coefficients
- standard errors
- R-squared
- causality warnings

---

## Project and Maintenance Documents

### [Project Vision](project_vision.md)

Explains the purpose, audience, values, and long-term direction of EconKit.

---

### [FAQ](faq.md)

Answers common questions about EconKit.

Good for users who want a quick explanation of the project.

---

### [Release Checklist](release_checklist.md)

A practical checklist for preparing future releases.

Use this before publishing a new version.

---

## Recommended Reading by User Type

## Beginner Student

Read:

1. [Project Vision](project_vision.md)
2. [Examples Guide](examples.md)
3. [Glossary](glossary.md)
4. [Troubleshooting](troubleshooting.md)

Then run:

```bash
python examples/analyze_macro_data.py
```

---

## Python User

Read:

1. [API Reference](api.md)
2. [Examples Guide](examples.md)
3. [Methodology](methodology.md)

Then try:

```python
from econkit import load_economic_data, analyze_macro_risk

data = load_economic_data("data/sample_economic_data.csv")
risk = analyze_macro_risk(data)
print(risk["summary"])
```

---

## CLI User

Read:

1. [CLI Guide](cli.md)
2. [Troubleshooting](troubleshooting.md)

Then try:

```bash
python src/econkit_cli.py features
python src/econkit_cli.py validate data/sample_economic_data.csv
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

---

## Contributor

Read:

1. [Architecture](architecture.md)
2. [API Reference](api.md)
3. [Methodology](methodology.md)
4. [Release Checklist](release_checklist.md)

Also read the repository-level files:

```text
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
CHANGELOG.md
```

---

## Instructor or Teaching Assistant

Read:

1. [Project Vision](project_vision.md)
2. [Examples Guide](examples.md)
3. [Methodology](methodology.md)
4. [Glossary](glossary.md)

EconKit can be used to teach:

- applied macroeconomic data analysis
- data cleaning
- reproducible reports
- scenario thinking
- simple forecasting
- regression interpretation
- GitHub-based project workflows

---

## Suggested Learning Path

A good learning sequence is:

```text
1. Read project_vision.md
2. Run examples/analyze_macro_data.py
3. Read examples.md
4. Run examples/analyze_macro_risk.py
5. Read methodology.md
6. Try CLI commands from cli.md
7. Read api.md
8. Modify an example script
9. Run tests
10. Create your own analysis
```

---

## Common Commands

Validate sample data:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Show available features:

```bash
python src/econkit_cli.py features
```

Generate a report:

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

Run macro risk analysis:

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

Generate scenarios:

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5 --stress-tests
```

Generate forecasts:

```bash
python src/econkit_cli.py forecast data/sample_economic_data.csv --output-dir outputs/forecasts --periods 5
```

Run regression:

```bash
python src/econkit_cli.py ols data/sample_economic_data.csv \
  --formula "inflation_rate ~ gdp_growth + unemployment_rate" \
  --output-dir outputs/regression
```

Run tests:

```bash
pytest
```

---

## Documentation Philosophy

EconKit documentation should be:

- clear
- practical
- beginner-friendly
- honest about limitations
- economically interpretable
- useful for GitHub readers
- useful for students
- useful for future contributors

Good documentation does not just explain what a function does.

It explains why the function exists and how to interpret the result.

---

## Educational Disclaimer

EconKit is designed for learning and exploratory economics data analysis.

It should not be interpreted as:

- investment advice
- an official forecast
- a central-bank policy model
- proof of causality
- a substitute for professional econometric software

Use EconKit as a transparent starting point for economic reasoning.
