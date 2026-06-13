# EconKit

EconKit is an open-source Python toolkit for beginner-friendly economics data analysis.

It helps students and early researchers move from a macroeconomic CSV file to:

- Summary statistics
- Charts
- Macro risk screening
- Monetary policy stance analysis
- Business-cycle diagnosis
- Scenario simulation
- Markdown and JSON outputs

## Why EconKit exists

Many economics students learn concepts such as GDP growth, inflation, unemployment, and interest rates, but struggle to connect those concepts with actual data workflows in Python. EconKit provides a simple, readable, and reusable toolkit for practicing that workflow.

## Main features

- Load macroeconomic CSV data
- Validate required columns
- Calculate summary statistics
- Find highest and lowest indicator years
- Create line charts
- Generate Markdown reports
- Classify macroeconomic risk
- Analyze monetary policy stance using a simple policy-rule benchmark
- Diagnose the business-cycle phase
- Simulate baseline, inflation shock, recession shock, and tight-policy scenarios
- Export Markdown, CSV, and JSON outputs

## Required dataset format

Your CSV should include these columns:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

A sample dataset is included at:

```text
data/sample_economic_data.csv
```

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate the sample dataset:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

Run the full analysis pipeline:

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

## CLI examples

Generate a report:

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

Analyze macro risk:

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

Analyze monetary policy stance:

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
```

Diagnose the business cycle:

```bash
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
```

Run macro scenarios:

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

## Python example

```python
from econkit import load_economic_data, analyze_macro_risk, analyze_monetary_policy_stance

data = load_economic_data("data/sample_economic_data.csv")

risk = analyze_macro_risk(data)
policy = analyze_monetary_policy_stance(data)

print(risk["summary"])
print(policy["summary"])
```

## Educational note

EconKit is designed for learning and teaching. The macro risk, monetary policy, business-cycle, and scenario tools use simple educational rules. They should not be interpreted as professional forecasts, investment advice, or official policy recommendations.

## Maintainer

This project is maintained by Gyujin Lee.

## License

This project is licensed under the MIT License.
