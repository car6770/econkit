# EconKit Methodology

This document explains the logic behind EconKit's macroeconomic diagnostics, scenario simulation, forecasting, and lightweight econometric tools.

EconKit is designed to be transparent.

That means users should be able to inspect the code, read the documentation, understand the assumptions, and reproduce the outputs.

---

## Purpose of This Document

EconKit includes tools that produce economic labels such as:

```text
Moderate macro risk
Tight monetary policy
Stable expansion
Elevated inflation pressure
Mixed macro regime
```

This document explains how those labels are produced.

The goal is not to claim that EconKit is a full professional forecasting model.

The goal is to make the reasoning clear.

---

## Methodological Philosophy

EconKit follows four methodological principles.

### 1. Transparency Over Complexity

EconKit prefers simple, inspectable logic over black-box models.

A user should be able to answer:

```text
Why did EconKit produce this result?
```

without needing hidden model weights, private datasets, or complicated software.

---

### 2. Educational Usefulness

EconKit is designed to help users learn applied economics.

The methodology should help users understand concepts such as:

- inflation pressure
- GDP growth conditions
- labor-market conditions
- monetary tightness
- policy gaps
- output-gap proxies
- scenario shocks
- regression interpretation
- forecast limitations

---

### 3. Reproducibility

Given the same dataset and parameters, EconKit should produce the same result.

This makes the toolkit useful for:

- class projects
- GitHub portfolio projects
- early research workflows
- teaching examples
- reproducible policy memo drafts

---

### 4. Honest Limitations

EconKit's models are simplified.

They are not:

- official forecasts
- central-bank policy models
- structural macroeconomic models
- investment advice
- causal identification strategies
- substitutes for professional econometric software

EconKit outputs should be interpreted as structured starting points for analysis.

---

# Required Macroeconomic Variables

The main macroeconomic workflow uses five variables:

```text
year
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

These variables are chosen because they summarize four major dimensions of macroeconomic conditions:

| Dimension | Variable |
|---|---|
| Output / growth | `gdp_growth` |
| Prices | `inflation_rate` |
| Labor market | `unemployment_rate` |
| Monetary / financial conditions | `interest_rate` |
| Time | `year` |

This structure is intentionally simple.

It allows users to practice macroeconomic analysis without needing a large database.

---

# Data Cleaning Methodology

EconKit's cleaning tools help convert a raw dataset into a consistent format.

## Column Name Cleaning

The function `clean_column_names` standardizes column names.

Examples:

```text
GDP Growth       -> gdp_growth
Inflation Rate   -> inflation_rate
Interest-Rate    -> interest_rate
Interest/Rate    -> interest_rate
```

This reduces errors caused by inconsistent formatting.

---

## Macro Dataset Cleaning

The function `clean_macro_dataset` applies several steps:

1. Clean column names
2. Convert required macro columns to numeric values
3. Convert `year` to integer
4. Drop rows with missing year
5. Drop duplicate years by keeping the latest observation
6. Sort observations by year

This makes the dataset ready for analysis.

---

## Validation

The function `validate_macro_dataset` checks whether the dataset is usable.

It verifies:

- required columns exist
- dataset is not empty
- required columns do not contain missing values
- `year` is numeric
- `year` does not contain duplicates

This is important because macroeconomic diagnostics can be misleading if the dataset is incomplete or malformed.

---

# Macro Risk Methodology

The macro risk model is a transparent rule-based diagnostic.

It uses four signals:

```text
inflation pressure
growth condition
labor market condition
monetary condition
```

Each signal is classified separately. Then the signals are combined into a risk score.

---

## Inflation Pressure Classification

Input:

```text
inflation_rate
```

Classification logic:

| Inflation Rate | Label |
|---|---|
| Missing | `Unknown` |
| Less than 1.0 | `Low` |
| 1.0 to less than 2.5 | `Normal` |
| 2.5 to less than 4.0 | `Elevated` |
| 4.0 or higher | `High` |

Interpretation:

- Low inflation may indicate weak demand or low price pressure.
- Normal inflation suggests moderate price conditions.
- Elevated inflation suggests rising price pressure.
- High inflation suggests major price pressure.

---

## Growth Condition Classification

Input:

```text
gdp_growth
```

Classification logic:

| GDP Growth | Label |
|---|---|
| Missing | `Unknown` |
| Less than 0.0 | `Contraction` |
| 0.0 to less than 1.5 | `Weak` |
| 1.5 to 3.0 | `Moderate` |
| Greater than 3.0 | `Strong` |

Interpretation:

- Negative growth indicates contraction.
- Weak growth may indicate slowdown.
- Moderate growth suggests stable expansion.
- Strong growth may suggest robust expansion.

---

## Labor Market Classification

Input:

```text
unemployment_rate
```

Classification logic:

| Unemployment Rate | Label |
|---|---|
| Missing | `Unknown` |
| Less than 3.0 | `Tight` |
| 3.0 to 4.0 | `Stable` |
| Greater than 4.0 to 5.0 | `Soft` |
| Greater than 5.0 | `Weak` |

Interpretation:

- Low unemployment suggests a tight labor market.
- Stable unemployment suggests normal labor conditions.
- Soft unemployment suggests some weakness.
- Weak unemployment suggests labor-market stress.

---

## Monetary Condition Classification

Input:

```text
interest_rate
```

Classification logic:

| Interest Rate | Label |
|---|---|
| Missing | `Unknown` |
| Less than 1.5 | `Accommodative` |
| 1.5 to less than 3.0 | `Neutral` |
| 3.0 or higher | `Tight` |

Interpretation:

- Low rates may stimulate demand.
- Moderate rates may be neutral.
- High rates may restrain demand.

---

## Macro Risk Score

EconKit assigns points based on risk signals.

### Inflation Points

| Inflation Pressure | Points |
|---|---|
| `High` | 2 |
| `Elevated` | 1 |
| Other | 0 |

### Growth Points

| Growth Condition | Points |
|---|---|
| `Contraction` | 2 |
| `Weak` | 1 |
| Other | 0 |

### Labor Market Points

| Labor Market | Points |
|---|---|
| `Weak` | 2 |
| `Soft` | 1 |
| Other | 0 |

### Monetary Condition Points

| Monetary Condition | Points |
|---|---|
| `Tight` | 1 |
| Other | 0 |

---

## Overall Macro Risk Classification

Total score:

```text
risk_score = inflation_points + growth_points + labor_points + monetary_points
```

Classification:

| Risk Score | Overall Risk |
|---|---|
| 0 | `Low` |
| 1 to 2 | `Moderate` |
| 3 to 4 | `Elevated` |
| 5 or higher | `High` |

---

## Why This Model Is Useful

The macro risk model is useful because it is:

- simple
- transparent
- easy to explain
- easy to test
- easy to modify
- useful for early-stage screening

It is not a substitute for a full macroeconomic forecasting model.

---

# Monetary Policy Methodology

EconKit's monetary policy analysis compares the actual interest rate with a simple policy-rule benchmark.

The goal is to classify whether monetary policy appears:

```text
Tight
Moderately Tight
Neutral
Moderately Accommodative
Accommodative
```

---

## Real Interest Rate

Approximate real interest rate:

```text
real_interest_rate = nominal_interest_rate - inflation_rate
```

Example:

```text
nominal interest rate = 3.5
inflation rate = 2.3

real interest rate = 1.2
```

This is a simple Fisher-style approximation.

EconKit also supports an exact calculation in the core function.

---

## Policy-Rule Benchmark

EconKit uses a transparent policy-rule benchmark:

```text
recommended_policy_rate =
neutral_interest_rate
+ inflation_weight × inflation_gap
+ growth_weight × growth_gap
```

where:

```text
inflation_gap = inflation_rate - target_inflation
growth_gap = gdp_growth - potential_growth
```

Default weights:

```text
inflation_weight = 0.5
growth_weight = 0.5
```

Default target inflation:

```text
target_inflation = 2.0
```

Potential growth and neutral interest rate can be estimated from recent data or provided by the user.

---

## Policy Gap

The policy gap is:

```text
policy_gap = actual_interest_rate - recommended_policy_rate
```

Interpretation:

| Policy Gap | Meaning |
|---|---|
| Positive | Actual rate is above benchmark |
| Negative | Actual rate is below benchmark |
| Near zero | Actual rate is close to benchmark |

---

## Policy Stance Classification

Classification:

| Policy Gap | Policy Stance |
|---|---|
| Greater than or equal to 0.75 | `Tight` |
| 0.25 to less than 0.75 | `Moderately Tight` |
| Greater than -0.25 and less than 0.25 | `Neutral` |
| -0.75 to -0.25 | `Moderately Accommodative` |
| Less than or equal to -0.75 | `Accommodative` |

---

## Interpretation Example

Suppose:

```text
actual interest rate = 3.50
recommended policy rate = 3.57
policy gap = -0.07
```

Because the gap is close to zero, EconKit classifies policy as:

```text
Neutral
```

This means the actual rate is close to the transparent benchmark under the selected assumptions.

---

## Important Caveat

The policy-rule benchmark is simplified.

Real monetary policy decisions may consider:

- financial stability
- exchange rates
- credit conditions
- expectations
- global shocks
- fiscal policy
- supply shocks
- central-bank communication
- uncertainty
- distributional effects

EconKit does not claim to replicate central-bank decision-making.

---

# Business-Cycle Methodology

EconKit diagnoses the latest business-cycle condition using:

```text
gdp_growth
estimated potential growth
output-gap proxy
inflation rate
```

---

## Potential Growth Estimate

By default, EconKit estimates potential growth as the recent average GDP growth.

Example:

```text
potential_growth = average of recent gdp_growth observations
```

This is a simple approximation.

It is not a structural estimate of potential output.

---

## Output-Gap Proxy

EconKit calculates:

```text
output_gap_proxy = gdp_growth - estimated_potential_growth
```

Interpretation:

| Output-Gap Proxy | Meaning |
|---|---|
| Positive | Growth is above recent baseline |
| Negative | Growth is below recent baseline |

This is a growth-gap proxy, not a full output gap.

---

## Business-Cycle Labels

Possible labels:

```text
Recession
Slowdown
Weak Recovery
Recovery
Stable Expansion
Expansion
Overheating
```

---

## Classification Logic

Simplified logic:

| Condition | Label |
|---|---|
| GDP growth < 0 | `Recession` |
| GDP growth < 1.0 and output gap < 0 | `Slowdown` |
| Inflation >= 3.0 and GDP growth >= 3.0 | `Overheating` |
| GDP growth between 1.5 and 3.0 | `Stable Expansion` |
| GDP growth > 3.0 | `Expansion` |
| Output gap > 0 | `Recovery` |
| Otherwise | `Weak Recovery` |

---

## Interpretation Example

If the latest observation is:

```text
gdp_growth = 2.0
estimated_potential_growth = 1.92
output_gap_proxy = 0.08
inflation_rate = 2.3
```

EconKit may classify the economy as:

```text
Stable Expansion
```

This means growth is positive and near a stable range.

---

# Inflation Pressure Methodology

EconKit's inflation pressure analysis includes:

```text
latest inflation rate
target inflation
inflation gap
recent average inflation
inflation momentum
pressure label
```

---

## Inflation Gap

```text
inflation_gap = inflation_rate - target_inflation
```

Example:

```text
inflation_rate = 2.3
target_inflation = 2.0

inflation_gap = 0.3
```

---

## Recent Average Inflation

EconKit calculates recent average inflation using a window.

Default:

```text
window = 3
```

Example:

```text
recent_average_inflation = average inflation over last 3 observations
```

---

## Inflation Momentum

```text
inflation_momentum = latest_inflation - previous_inflation
```

Momentum label:

| Momentum | Label |
|---|---|
| Greater than 0.25 | `Rising` |
| Less than -0.25 | `Falling` |
| Otherwise | `Stable` |

---

## Inflation Pressure Label

The pressure label uses the same logic as macro risk inflation pressure:

| Inflation Rate | Label |
|---|---|
| Less than 1.0 | `Low` |
| 1.0 to less than 2.5 | `Normal` |
| 2.5 to less than 4.0 | `Elevated` |
| 4.0 or higher | `High` |

---

# Policy-Mix Methodology

Policy-mix analysis combines four diagnostics:

```text
macro risk
monetary policy stance
business-cycle phase
inflation pressure
```

The result is a broad macro regime label.

---

## Policy-Mix Score

EconKit adds points from several sources.

### Macro Risk Contribution

| Overall Macro Risk | Points |
|---|---|
| `High` | 3 |
| `Elevated` | 2 |
| `Moderate` | 1 |
| `Low` | 0 |

### Policy Stance Contribution

| Policy Stance | Points |
|---|---|
| `Tight` | 1 |
| `Accommodative` | 1 |
| Other | 0 |

### Business Cycle Contribution

| Business Cycle | Points |
|---|---|
| `Recession` | 2 |
| `Overheating` | 2 |
| `Slowdown` | 1 |
| Other | 0 |

### Inflation Contribution

| Inflation Pressure | Points |
|---|---|
| `High` | 2 |
| `Elevated` | 1 |
| Other | 0 |

---

## Policy-Mix Regime

Classification:

| Score | Regime |
|---|---|
| 0 to 1 | `Stable macro regime` |
| 2 to 3 | `Mixed macro regime` |
| 4 to 5 | `Elevated tension macro regime` |
| 6 or higher | `High tension macro regime` |

---

## Interpretation

A `Stable macro regime` suggests that the latest macro data do not show strong warning signs.

A `Mixed macro regime` suggests some tensions exist but are not severe.

An `Elevated tension macro regime` suggests multiple warning signs.

A `High tension macro regime` suggests broad macroeconomic stress.

---

# Scenario Simulation Methodology

EconKit's scenario simulator creates future paths for:

```text
gdp_growth
inflation_rate
unemployment_rate
interest_rate
```

It is a transparent rule-based simulator.

It is not a structural macroeconomic model.

---

## Scenario Inputs

Users can specify:

```text
demand_shock
supply_shock
policy_shock
years
```

Interpretation:

| Shock | Effect |
|---|---|
| `demand_shock` | Positive values raise growth and inflation |
| `supply_shock` | Positive values raise inflation and reduce growth |
| `policy_shock` | Positive values raise interest rates |

---

## Shock Decay

Shocks decay over time.

EconKit uses:

```text
shock_decay = 0.65 ** (step - 1)
```

This means the shock is strongest in the first projected year and gradually weakens.

---

## Interest Rate Path

The simulated interest rate responds to:

```text
neutral interest rate
inflation deviation from target
growth deviation from potential
policy shock
```

Simplified form:

```text
interest_rate =
neutral_interest_rate
+ 0.45 × inflation_gap
+ 0.20 × growth_gap
+ policy_shock
```

The rate is bounded below by zero.

---

## GDP Growth Path

GDP growth responds to:

```text
previous GDP growth
potential growth
demand shock
interest-rate tightening
supply shock
```

Simplified form:

```text
gdp_growth =
0.55 × previous_gdp_growth
+ 0.45 × potential_growth
+ demand_shock
- effect_of_tight_interest_rates
- effect_of_supply_shock
```

---

## Inflation Path

Inflation responds to:

```text
previous inflation
target inflation
positive growth gap
supply shock
tight interest rates
```

Simplified form:

```text
inflation =
0.60 × previous_inflation
+ 0.40 × target_inflation
+ demand_pressure
+ supply_shock_effect
- tight_policy_effect
```

---

## Unemployment Path

Unemployment responds to:

```text
previous unemployment
normal unemployment
growth relative to potential
```

Simplified form:

```text
unemployment =
0.70 × previous_unemployment
+ 0.30 × normal_unemployment
- 0.35 × growth_gap
```

Unemployment is bounded below by zero.

---

## Default Scenarios

EconKit includes:

| Scenario | Shocks |
|---|---|
| `baseline` | No shock |
| `inflation_shock` | Positive supply shock |
| `recession_shock` | Negative demand shock |
| `tight_policy` | Positive policy shock |

---

## Stress-Test Scenarios

EconKit also includes:

| Scenario | Description |
|---|---|
| `stagflation` | Negative demand shock plus positive supply shock |
| `soft_landing` | Mild demand and supply improvement |
| `hard_landing` | Strong negative demand shock |
| `supply_recovery` | Negative supply shock pressure |
| `policy_mistake` | Negative demand shock plus strong policy shock |

---

## Scenario Comparison

EconKit compares scenarios using final-year outcomes:

```text
final_gdp_growth
final_inflation_rate
final_unemployment_rate
final_interest_rate
overall_risk
risk_score
```

This helps users compare which scenario produces the most stress.

---

# Forecasting Methodology

EconKit includes two simple forecasting methods:

```text
AR(1)
moving average
```

These are baseline forecasting tools.

They are intentionally simple and transparent.

---

## AR(1) Forecast

An AR(1) model estimates:

```text
y_t = intercept + phi × y_(t-1)
```

Then it uses the estimated relationship to forecast future values.

Interpretation:

- `intercept` is the baseline component.
- `phi` measures persistence.
- If `phi` is high, the variable depends strongly on its previous value.
- If `phi` is low, the variable reverts more quickly.

---

## Moving-Average Forecast

A moving-average forecast uses:

```text
forecast = average of recent observations
```

Default window:

```text
window = 3
```

This is useful as a simple baseline.

---

## Forecasting Limitations

Forecasts can be sensitive to:

- small datasets
- structural breaks
- unusual shocks
- policy changes
- global events
- measurement changes

EconKit forecasts should not be treated as official forecasts.

---

# OLS Regression Methodology

EconKit includes a lightweight ordinary least squares engine.

---

## Regression Model

OLS estimates:

```text
y = Xβ + ε
```

where:

| Symbol | Meaning |
|---|---|
| `y` | dependent variable |
| `X` | independent variables |
| `β` | coefficients |
| `ε` | residual |

---

## Coefficients

A coefficient estimates the association between an independent variable and the dependent variable, holding included variables fixed.

Example:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

The coefficient on `gdp_growth` describes how inflation is associated with GDP growth in the sample, controlling for unemployment.

---

## Standard Errors

EconKit supports:

```text
conventional standard errors
White robust standard errors
```

Robust standard errors are useful when residual variance may not be constant.

---

## R-Squared

R-squared measures the share of variation in the dependent variable explained by the model.

Important:

```text
High R-squared does not prove causality.
```

---

## Formula Interface

EconKit supports formulas such as:

```text
inflation_rate ~ gdp_growth + unemployment_rate
```

This is parsed into:

```text
dependent variable = inflation_rate
independent variables = gdp_growth, unemployment_rate
```

---

## Regression Limitations

OLS results may be misleading if there is:

- omitted variable bias
- reverse causality
- measurement error
- small sample size
- nonstationarity
- multicollinearity
- structural breaks
- autocorrelation
- endogeneity

EconKit regression is useful for teaching and exploration, not for automatic causal claims.

---

# Report Generation Methodology

EconKit reports are designed to be readable.

Reports typically include:

```text
dataset overview
executive summary
summary statistics
indicator highlights
correlation matrix
macro risk analysis
monetary policy stance
business-cycle diagnosis
inflation pressure
scenario comparison
educational notes
```

Reports are saved as Markdown because Markdown is:

- readable in GitHub
- easy to edit
- easy to convert
- version-control friendly
- beginner-friendly

---

# JSON Output Methodology

Many EconKit outputs can be saved as JSON.

JSON is useful for:

- reproducibility
- dashboards
- APIs
- notebooks
- automated workflows
- future web applications

EconKit uses structured dictionaries so that JSON outputs are easy to inspect.

---

# How to Modify Thresholds

Many EconKit methods are intentionally simple.

Advanced users can modify thresholds directly in the source code.

Examples:

```python
classify_inflation_pressure
classify_growth_condition
classify_labor_market
classify_monetary_condition
classify_policy_stance
classify_business_cycle_phase
```

Recommended practice:

1. Change one threshold at a time.
2. Update tests.
3. Update documentation.
4. Explain the economic reason for the change.
5. Avoid hiding assumptions.

---

# How to Interpret EconKit Results

A good EconKit interpretation should be careful.

Good:

```text
EconKit classifies inflation pressure as elevated based on the latest inflation rate.
```

Good:

```text
Under the selected assumptions, the actual interest rate is close to the policy-rule benchmark.
```

Good:

```text
The stress-test scenario produces higher macro risk than the baseline scenario.
```

Too strong:

```text
Inflation will definitely rise.
```

Too strong:

```text
The central bank must cut rates.
```

Too strong:

```text
This regression proves that interest rates cause unemployment.
```

---

# Summary

EconKit's methodology is built around:

```text
transparent rules
simple calculations
reproducible outputs
educational interpretation
honest limitations
```

The toolkit is designed to help users move from raw economic data to structured economic reasoning.

It should be used as a learning and exploratory analysis tool, not as an official forecasting or policy system.
