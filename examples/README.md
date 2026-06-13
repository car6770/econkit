# EconKit Examples

This folder contains runnable example scripts.

Run examples from the project root.

---

## Available Examples

```text
analyze_macro_data.py
analyze_macro_risk.py
generate_report.py
run_macro_scenarios.py
run_forecasting.py
run_regression.py
```

---

## Recommended Order

```bash
python examples/analyze_macro_data.py
python examples/analyze_macro_risk.py
python examples/generate_report.py
python examples/run_macro_scenarios.py
python examples/run_forecasting.py
python examples/run_regression.py
```

---

## Input Data

All examples use:

```text
data/sample_economic_data.csv
```

---

## Output Folder

Examples save generated files under:

```text
outputs/examples/
```

The `outputs/` folder is ignored by Git because generated files should usually not be committed.

---

## Learning Goal

The examples show how to use EconKit for:

- loading data
- cleaning data
- validating data
- calculating statistics
- creating charts
- diagnosing macro risk
- generating reports
- simulating scenarios
- forecasting
- running regression

---

## Troubleshooting

If an example cannot import EconKit, make sure you are running it from the repository root.

Correct:

```bash
python examples/analyze_macro_data.py
```

Incorrect:

```bash
cd examples
python analyze_macro_data.py
```
