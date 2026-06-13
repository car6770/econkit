# Data Folder

This folder contains sample datasets used by EconKit examples and tests.

---

## Included Dataset

```text
sample_economic_data.csv
```

This is a small educational macroeconomic dataset.

It includes:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

---

## Purpose

The sample dataset is used for:

- examples
- documentation
- tests
- CLI demonstrations
- report generation
- scenario simulation
- forecasting
- regression examples

---

## Important Note

The sample dataset is designed for learning and demonstration.

It should not be interpreted as an official macroeconomic dataset.

For real research, users should replace it with data from reliable sources and document the source clearly.

---

## Required Format

Most EconKit macro functions expect:

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
```

---

## Adding New Data

When adding a new dataset:

- use clear column names
- avoid private data
- avoid sensitive data
- document the data source
- explain whether the data is real, simulated, or educational
- keep files small when possible
