# EconKit CLI Guide

EconKit includes a command-line interface for beginner-friendly economics data analysis.

## Required dataset format

The input CSV file should include:

- `year`
- `gdp_growth`
- `inflation_rate`
- `unemployment_rate`
- `interest_rate`

## Commands

### Validate a dataset

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

### Generate a report

```bash
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
```

### Analyze macro risk

```bash
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
```

### Analyze monetary policy stance

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
```

Optional assumptions:

```bash
python src/econkit_cli.py policy data/sample_economic_data.csv \
  --target-inflation 2.0 \
  --neutral-interest-rate 2.5 \
  --potential-growth 2.0
```

### Diagnose the business cycle

```bash
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
```

### Run scenarios

```bash
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
```

### Run everything

```bash
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

## Installed command usage

After installation, users can run:

```bash
econkit all data/sample_economic_data.csv --output-dir outputs --years 5
```

## Educational note

The macro risk, monetary policy, business-cycle, and scenario tools are educational rules of thumb. They are not professional forecasts or official policy recommendations.
