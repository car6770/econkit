# Contributing to EconKit

Thank you for your interest in contributing to EconKit.

EconKit is a Python toolkit for economics data analysis, macroeconomic diagnostics, scenario simulation, forecasting, lightweight econometrics, and automated reporting.

The project is designed to be useful for:

- economics students
- early researchers
- instructors
- policy-minded analysts
- people learning applied data analysis with Python

This guide explains how to contribute in a way that keeps the project clean, readable, tested, and beginner-friendly.

---

## Project Philosophy

EconKit values:

1. **Clarity**
   - Code should be readable.
   - Function names should explain what they do.
   - Economic logic should be transparent.

2. **Reproducibility**
   - A user should be able to run the same dataset and get the same result.
   - Outputs should be saved in predictable locations.
   - CLI commands should be documented.

3. **Beginner-friendliness**
   - EconKit should help students learn.
   - Error messages should be understandable.
   - Examples should be practical.

4. **Professional structure**
   - Features should be tested.
   - Documentation should be updated.
   - Public functions should remain stable when possible.

5. **Educational honesty**
   - Simplified models should be described as simplified.
   - Forecasts and scenarios should not be presented as official predictions.
   - Policy analysis should not be presented as professional policy advice.

---

## Ways to Contribute

You can contribute by:

- fixing bugs
- improving documentation
- adding examples
- improving tests
- adding new economic indicators
- improving charts
- adding new CLI commands
- improving data validation
- adding regression diagnostics
- adding forecasting tools
- improving scenario simulation
- improving report generation
- suggesting better economic interpretations

Small contributions are welcome.

---

## Project Structure

Typical project structure:

```text
econkit/
  .github/
    workflows/
      tests.yml
  data/
    sample_economic_data.csv
  docs/
    cli.md
  examples/
    analyze_macro_data.py
    analyze_macro_risk.py
    generate_report.py
    run_macro_scenarios.py
  outputs/
  src/
    econkit.py
    econkit_cli.py
  tests/
    test_cli.py
    test_econkit.py
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  LICENSE
  pyproject.toml
  requirements.txt
```

Main files:

| File | Purpose |
|---|---|
| `src/econkit.py` | Core EconKit functions |
| `src/econkit_cli.py` | Command-line interface |
| `tests/test_econkit.py` | Tests for core functions |
| `tests/test_cli.py` | Tests for CLI compatibility |
| `README.md` | Main public project documentation |
| `docs/cli.md` | Detailed CLI guide |
| `CHANGELOG.md` | Release history |
| `requirements.txt` | Runtime and test dependencies |
| `pyproject.toml` | Python package configuration |

---

## Development Setup

Clone the repository:

```bash
git clone https://github.com/car6770/econkit.git
cd econkit
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional editable install:

```bash
pip install -e .
```

Optional development install:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run the CLI directly:

```bash
python src/econkit_cli.py features
```

---

## Before Making Changes

Before changing code, check that the current project works:

```bash
pytest
```

Then run a basic CLI command:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
```

If both work, you have a stable starting point.

---

## Coding Guidelines

### 1. Keep Functions Clear

Prefer readable names:

```python
def analyze_macro_risk(data):
    ...
```

Avoid vague names:

```python
def do_analysis(x):
    ...
```

A user should understand the function's purpose from the name.

---

### 2. Keep Economic Logic Transparent

EconKit should not hide economic assumptions.

Good:

```python
inflation_gap = inflation_rate - target_inflation
growth_gap = gdp_growth - potential_growth
```

Less helpful:

```python
score = model.run(x)
```

If a model uses thresholds, weights, or simplified rules, make them visible.

---

### 3. Avoid Unnecessary Dependencies

EconKit should stay easy to install.

Core dependencies should remain lightweight:

```text
numpy
pandas
matplotlib
tabulate
```

Before adding a new dependency, ask:

- Is it necessary?
- Can this be done with pandas, numpy, or matplotlib?
- Will it make installation harder for beginners?
- Will it slow down GitHub Actions?
- Is it optional?

Heavy dependencies should usually be optional.

---

### 4. Preserve Backward Compatibility

Avoid breaking existing function names unless necessary.

If a key or function name changes, consider supporting both names.

Example:

```python
analysis.get("business_cycle_phase", analysis.get("phase"))
```

This keeps older tests and examples working.

---

### 5. Return Structured Results

Analysis functions should return dictionaries with stable keys.

Example:

```python
{
    "latest_year": 2024,
    "overall_risk": "Moderate",
    "risk_score": 1,
    "signals": {...},
    "summary": "..."
}
```

This makes the function useful for:

- tests
- CLI output
- Markdown reports
- JSON export
- notebooks
- future dashboards

---

### 6. Write Beginner-Friendly Errors

Good:

```python
raise ValueError("Missing required columns: ['gdp_growth']")
```

Bad:

```python
raise Exception("Bad data")
```

Error messages should help users fix the problem.

---

### 7. Keep Reports Readable

Markdown reports should have:

- a clear title
- short sections
- bullet points
- interpretation text
- educational notes when needed

Reports should not only dump raw data.

---

## Testing Guidelines

All new features should include tests when possible.

Run:

```bash
pytest
```

Tests should check:

- function output structure
- important values
- expected file creation
- expected CLI behavior
- error handling for missing columns or bad input

---

## Example Test Style

Good test:

```python
def test_analyze_macro_risk_returns_expected_structure():
    data = make_sample_macro_data()

    analysis = analyze_macro_risk(data)

    assert analysis["latest_year"] == 2024
    assert "signals" in analysis
    assert "overall_risk" in analysis
    assert "summary" in analysis
```

This test checks structure without being too fragile.

---

## Avoid Overly Fragile Tests

Avoid tests that break when wording changes slightly.

Fragile:

```python
assert analysis["summary"] == "In 2024, the economy is exactly..."
```

Better:

```python
assert "summary" in analysis
assert "2024" in analysis["summary"]
```

Tests should protect functionality, not block reasonable wording improvements.

---

## CLI Contribution Guidelines

When adding a CLI command:

1. Add a command function.
2. Add parser configuration in `build_parser`.
3. Save outputs in a predictable folder.
4. Print a short success message.
5. Document the command in `README.md`.
6. Document the command in `docs/cli.md`.
7. Add or update tests if possible.

Example command structure:

```python
def command_example(args):
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    # analysis here

    print("Example analysis completed.")
```

---

## Documentation Guidelines

Update documentation when you change:

- public functions
- CLI commands
- output file names
- required columns
- installation instructions
- project structure
- examples
- assumptions behind analysis tools

Important documentation files:

```text
README.md
docs/cli.md
CHANGELOG.md
```

---

## Changelog Guidelines

When adding a meaningful change, update `CHANGELOG.md`.

Use sections such as:

```markdown
### Added
### Changed
### Fixed
### Removed
### Documentation
```

Example:

```markdown
### Added

- Added inflation pressure diagnosis.
- Added CLI command for inflation analysis.
```

---

## Data Guidelines

Sample datasets should be:

- small
- readable
- safe to share publicly
- easy to understand
- compatible with tests
- stored in `data/`

Do not include private, licensed, confidential, or sensitive datasets.

---

## Example Dataset Format

```csv
year,gdp_growth,inflation_rate,unemployment_rate,interest_rate
2020,-0.7,0.5,4.0,0.5
2021,4.3,2.5,3.7,1.0
2022,2.6,5.1,3.0,3.25
2023,1.4,3.6,2.7,3.50
2024,2.0,2.3,2.8,3.50
```

---

## Economic Interpretation Guidelines

When contributing analysis logic, be careful with wording.

Good:

```text
EconKit classifies this as elevated inflation pressure based on transparent thresholds.
```

Avoid:

```text
Inflation will definitely remain high.
```

EconKit should provide transparent diagnostics, not overconfident predictions.

---

## Forecasting Guidelines

Forecasting tools should:

- clearly state the method
- return a structured table
- avoid overclaiming accuracy
- work with small educational datasets when possible
- fail gracefully when there is not enough data

Forecasts should be described as baseline projections, not official predictions.

---

## Scenario Guidelines

Scenario tools should:

- show scenario names clearly
- use transparent shock assumptions
- generate reproducible outputs
- allow scenario comparison
- include educational notes

Scenario names should be readable:

```text
baseline
inflation_shock
recession_shock
tight_policy
stagflation
soft_landing
hard_landing
supply_recovery
policy_mistake
```

---

## Regression Guidelines

Regression tools should:

- support clear variable names
- return coefficients
- return standard errors
- return t-statistics
- return fitted values and residuals
- return R-squared
- provide Markdown output when possible

Regression output should be used for exploratory analysis and teaching.

---

## Pull Request Checklist

Before submitting a pull request, check:

- [ ] The code runs locally.
- [ ] `pytest` passes.
- [ ] New functions have clear names.
- [ ] New outputs are documented.
- [ ] CLI commands are documented if added.
- [ ] README is updated if needed.
- [ ] `docs/cli.md` is updated if needed.
- [ ] `CHANGELOG.md` is updated if needed.
- [ ] No private data is included.
- [ ] The contribution keeps EconKit beginner-friendly.

---

## Commit Message Examples

Good commit messages:

```text
Add inflation pressure diagnosis
Improve scenario comparison report
Fix CLI output path handling
Update README examples
Add regression report tests
```

Less helpful commit messages:

```text
fix
update
stuff
changes
```

---

## Issue Guidelines

When opening an issue, include:

- what you tried
- what happened
- what you expected
- the command you ran
- the error message
- your operating system if relevant
- your Python version if relevant

Example:

```markdown
I ran:

python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy

Expected:

A monetary policy report.

Got:

ValueError: Missing required columns: ['interest_rate']
```

---

## Feature Request Guidelines

For feature requests, explain:

- what problem the feature solves
- who would use it
- what input it needs
- what output it should produce
- whether it belongs in core Python API, CLI, or documentation

Example:

```markdown
Feature request: Add forecast evaluation metrics.

Problem:
Users can generate forecasts but cannot compare forecast accuracy.

Suggested output:
MAE, RMSE, and MAPE table.

Where:
Python API and CLI.
```

---

## Style Notes

EconKit should sound professional but not intimidating.

Preferred tone:

```text
clear
educational
transparent
practical
```

Avoid:

```text
overly technical explanations without examples
overconfident forecasting claims
black-box model language
unnecessary jargon
```

---

## Security and Privacy

Do not commit:

- private datasets
- credentials
- API keys
- passwords
- personal information
- confidential research data
- licensed datasets that cannot be redistributed

If a dataset is needed for an example, use a small synthetic dataset.

---

## License

By contributing to EconKit, you agree that your contributions will be licensed under the MIT License.

See:

```text
LICENSE
```

---

## Educational Disclaimer

EconKit is designed for educational and exploratory economic analysis.

It is not:

- an official forecasting model
- a central-bank policy model
- a source of investment advice
- a substitute for professional econometric software
- a source of official policy recommendations

Contributions should preserve this distinction.

---

## Thank You

Thank you for helping improve EconKit.

The goal is to build a practical, transparent, and beginner-friendly economics toolkit that helps users learn by doing real analysis.
