# EconKit Glossary

This glossary explains common economics, data-analysis, and EconKit terms in beginner-friendly language.

The goal is to make EconKit easier to use for students and early researchers.

---

# A

## Accommodative Monetary Policy

Monetary policy is accommodative when interest rates are relatively low and policy supports economic activity.

In EconKit, a policy stance may be classified as:

```text
Accommodative
Moderately Accommodative
Neutral
Moderately Tight
Tight
```

---

## Adjusted R-Squared

Adjusted R-squared is a regression fit measure that adjusts for the number of independent variables.

It is useful because regular R-squared usually increases when more variables are added, even if those variables are not very useful.

---

## AR(1)

AR(1) means autoregressive model of order 1.

Simple idea:

```text
today's value depends partly on yesterday's value
```

In EconKit, AR(1) is used as a simple transparent forecasting method.

---

# B

## Baseline Scenario

A baseline scenario is a simple future path that assumes recent conditions continue without a major shock.

In EconKit, baseline scenarios are used as reference cases.

---

## Business Cycle

The business cycle describes expansions and contractions in economic activity.

Common phases include:

```text
Recession
Slowdown
Recovery
Stable Expansion
Expansion
Overheating
```

EconKit uses GDP growth, inflation, and an output-gap proxy to classify the business-cycle phase.

---

# C

## Causal Interpretation

A causal interpretation claims that one variable causes another.

Example:

```text
Higher interest rates cause lower inflation.
```

Regression alone does not prove causality.

A causal claim usually requires a research design.

---

## CLI

CLI means command-line interface.

EconKit's CLI lets users run commands such as:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

---

## Coefficient

A regression coefficient measures the estimated relationship between an independent variable and the dependent variable.

Example:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

The coefficient on `gdp_growth` describes the association between GDP growth and inflation, holding unemployment fixed.

---

## Correlation

Correlation measures how two variables move together.

A positive correlation means two variables tend to move in the same direction.

A negative correlation means two variables tend to move in opposite directions.

Correlation does not prove causality.

---

# D

## Data Cleaning

Data cleaning means preparing raw data for analysis.

Examples:

- fixing column names
- converting values to numbers
- removing duplicate years
- checking missing values
- sorting by year

EconKit provides cleaning functions such as:

```python
clean_column_names
clean_macro_dataset
coerce_numeric_columns
```

---

## Data Validation

Data validation means checking whether a dataset is usable.

EconKit checks:

- required columns
- missing values
- duplicate years
- empty datasets
- numeric year column

Main function:

```python
validate_macro_dataset
```

---

## Dependent Variable

The dependent variable is the outcome variable in a regression.

Example:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

Here, `inflation_rate` is the dependent variable.

---

# E

## Econometrics

Econometrics uses statistical methods to study economic data.

EconKit includes lightweight econometric tools, especially simple OLS regression.

---

## Elevated Inflation

Elevated inflation means inflation is above normal but not necessarily extremely high.

In EconKit's default classification:

```text
2.5 <= inflation_rate < 4.0
```

is classified as:

```text
Elevated
```

---

## Endogeneity

Endogeneity occurs when an explanatory variable is related to the regression error term.

It can make regression coefficients misleading.

Common causes:

- omitted variables
- reverse causality
- measurement error
- simultaneity

EconKit regression tools do not automatically solve endogeneity.

---

# F

## Forecast

A forecast is a projection of future values.

EconKit includes simple forecasting tools:

```python
forecast_ar1
forecast_moving_average
generate_forecast_table
```

Forecasts are educational baseline projections, not official predictions.

---

## Formula Interface

A formula interface allows regression to be written like this:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

EconKit parses this into:

```text
dependent variable: inflation_rate
independent variables: gdp_growth, unemployment_rate
```

---

# G

## GDP Growth

GDP growth measures how fast an economy is expanding or contracting.

Positive GDP growth means output is increasing.

Negative GDP growth means output is decreasing.

EconKit uses:

```text
gdp_growth
```

as one of its required macro variables.

---

## Growth Condition

Growth condition is EconKit's label for the state of GDP growth.

Possible labels:

```text
Contraction
Weak
Moderate
Strong
Unknown
```

---

# H

## Hard Landing

A hard landing is a scenario where economic growth slows sharply or turns negative.

In EconKit, a hard landing stress test represents a strong negative demand shock.

---

## High Macro Risk

High macro risk means multiple macroeconomic warning signs appear at the same time.

Examples:

- high inflation
- weak growth
- weak labor market
- tight monetary conditions

---

# I

## Independent Variable

An independent variable is an explanatory variable in a regression.

Example:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

Here, `gdp_growth` and `unemployment_rate` are independent variables.

---

## Inflation

Inflation measures the rate at which prices increase.

EconKit uses:

```text
inflation_rate
```

as one of its required macro variables.

---

## Inflation Gap

Inflation gap is the difference between actual inflation and target inflation.

Formula:

```text
inflation_gap = inflation_rate - target_inflation
```

---

## Inflation Momentum

Inflation momentum measures whether inflation is rising, falling, or stable compared with the previous observation.

EconKit labels momentum as:

```text
Rising
Falling
Stable
```

---

## Inflation Pressure

Inflation pressure is EconKit's classification of the latest inflation condition.

Possible labels:

```text
Low
Normal
Elevated
High
Unknown
```

---

## Interest Rate

The interest rate summarizes monetary and financial conditions.

EconKit uses:

```text
interest_rate
```

as one of its required macro variables.

---

# L

## Labor Market

The labor market refers to employment and unemployment conditions.

EconKit uses:

```text
unemployment_rate
```

to classify labor-market conditions.

---

## Lightweight Regression

Lightweight regression means a simple regression tool designed for learning and exploration.

EconKit's regression module is intentionally simpler than professional econometrics packages.

---

# M

## Macro Diagnostics

Macro diagnostics are structured summaries of macroeconomic conditions.

EconKit diagnostics include:

```text
macro risk
monetary policy stance
business cycle
inflation pressure
policy mix
```

---

## Macro Risk

Macro risk is EconKit's summary of broad economic warning signs.

It combines:

- inflation pressure
- growth condition
- labor-market condition
- monetary condition

---

## Monetary Condition

Monetary condition describes whether interest rates are low, moderate, or high.

EconKit labels monetary conditions as:

```text
Accommodative
Neutral
Tight
Unknown
```

---

## Monetary Policy Stance

Monetary policy stance describes whether policy appears tight, neutral, or accommodative relative to a benchmark.

EconKit estimates this using a transparent policy-rule benchmark.

---

## Moving Average

A moving average uses the recent average of a variable.

In forecasting, EconKit uses a moving average as a simple baseline projection.

---

# N

## Neutral Interest Rate

The neutral interest rate is a benchmark rate that is neither strongly stimulating nor strongly restraining the economy.

EconKit uses it as part of monetary policy stance analysis.

---

## Nonstationarity

Nonstationarity means a time series has changing statistical properties over time.

This can affect regression and forecasting.

EconKit does not automatically solve nonstationarity issues.

---

# O

## OLS

OLS means ordinary least squares.

It is a common regression method that estimates coefficients by minimizing squared residuals.

EconKit includes:

```python
run_ols
run_ols_formula
regression_report
```

---

## Output Gap

A full output gap measures the difference between actual output and potential output.

EconKit uses a simplified growth-gap proxy:

```text
output_gap_proxy = gdp_growth - estimated_potential_growth
```

---

## Overheating

Overheating means the economy may be growing strongly while inflation pressure is also high.

In EconKit, overheating is one possible business-cycle label.

---

# P

## Policy Gap

Policy gap is the difference between the actual interest rate and EconKit's benchmark policy-rule rate.

Formula:

```text
policy_gap = actual_interest_rate - recommended_policy_rate
```

Positive gap:

```text
policy may be tighter than benchmark
```

Negative gap:

```text
policy may be more accommodative than benchmark
```

---

## Policy Mix

Policy mix combines several macro diagnostics into one broad regime.

EconKit combines:

- macro risk
- monetary policy stance
- business-cycle phase
- inflation pressure

---

## Policy Rule

A policy rule is a simplified benchmark for interest-rate policy.

EconKit's policy-rule benchmark uses:

- neutral interest rate
- inflation gap
- growth gap

---

## Potential Growth

Potential growth is a simple estimate of normal or sustainable growth.

EconKit estimates it using recent average GDP growth unless the user provides another value.

---

# R

## Real Interest Rate

The real interest rate adjusts the nominal interest rate for inflation.

Approximate formula:

```text
real_interest_rate = nominal_interest_rate - inflation_rate
```

---

## Recession

A recession is a period of contracting economic activity.

In EconKit, negative GDP growth is classified as a recession signal.

---

## Regression

Regression estimates the relationship between variables.

Example:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

Regression can show association, but it does not automatically prove causality.

---

## Residual

A residual is the difference between the actual value and the fitted value in a regression.

Formula:

```text
residual = actual value - fitted value
```

---

## Risk Score

Risk score is EconKit's numeric macro risk score.

Higher score means more warning signs.

---

## Robust Standard Errors

Robust standard errors adjust for possible heteroskedasticity.

EconKit supports simple White robust standard errors in OLS.

---

# S

## Scenario Simulation

Scenario simulation creates possible future paths under different assumptions.

EconKit scenarios can include:

- demand shocks
- supply shocks
- policy shocks

---

## Shock

A shock is an unexpected change in economic conditions.

Examples:

- demand shock
- supply shock
- policy shock

---

## Soft Landing

A soft landing is a scenario where inflation cools without a major growth collapse.

In EconKit, this is one of the stress-test scenarios.

---

## Stagflation

Stagflation means weak growth and high inflation at the same time.

It is often considered a difficult macroeconomic environment.

---

## Standard Error

A standard error measures uncertainty around an estimated regression coefficient.

Smaller standard errors usually mean more precise estimates.

---

## Structural Break

A structural break occurs when the relationship between variables changes over time.

Examples:

- pandemic shock
- financial crisis
- major policy regime change
- war
- new technology
- institutional change

Simple forecasts and regressions can perform poorly when structural breaks occur.

---

# T

## Target Inflation

Target inflation is the inflation rate that a central bank or policy framework aims for.

EconKit's default target inflation is:

```text
2.0
```

---

## Tight Monetary Policy

Tight monetary policy means interest rates are relatively high and may restrain economic activity.

---

## T-Statistic

A t-statistic is a regression statistic calculated as:

```text
coefficient / standard error
```

It helps evaluate how large an estimate is relative to its uncertainty.

---

# U

## Unemployment Rate

The unemployment rate measures the share of the labor force that is unemployed.

EconKit uses:

```text
unemployment_rate
```

as one of its required macro variables.

---

# V

## Validation

Validation checks whether a dataset is usable before analysis.

Main EconKit function:

```python
validate_macro_dataset
```

---

# Z

## Z-Score

A z-score measures how far a value is from the mean in standard deviation units.

Formula:

```text
z_score = (value - mean) / standard_deviation
```

EconKit can create z-score columns for selected indicators.

---

# Summary

This glossary is designed to help users understand EconKit outputs and documentation.

When using EconKit, remember:

```text
clear interpretation is as important as correct calculation
```

EconKit should help users explain economic data carefully, transparently, and honestly.
