# Changelog

All notable changes to EconKit are documented in this file.

EconKit follows a practical release-history format inspired by Keep a Changelog.
The project uses semantic versioning-style labels when possible.

---

## [1.1.0] - Professional Macro Toolkit Upgrade

### Added

- Added professional macroeconomic diagnostics workflow.
- Added full macro risk analysis.
- Added monetary policy stance analysis.
- Added business-cycle diagnosis.
- Added inflation pressure diagnosis.
- Added integrated policy-mix analysis.
- Added macro scenario simulation.
- Added default scenario set:
  - `baseline`
  - `inflation_shock`
  - `recession_shock`
  - `tight_policy`
- Added stress-test scenario set:
  - `stagflation`
  - `soft_landing`
  - `hard_landing`
  - `supply_recovery`
  - `policy_mistake`
- Added scenario comparison table generation.
- Added AR(1) forecasting.
- Added moving-average forecasting.
- Added multi-indicator forecast table generation.
- Added lightweight OLS regression engine.
- Added simple formula interface for regression:
  - Example: `inflation_rate ~ gdp_growth + unemployment_rate`
- Added conventional OLS standard errors.
- Added White heteroskedasticity-robust standard errors.
- Added regression Markdown report generation.
- Added data-quality profile.
- Added data-quality Markdown report.
- Added data-quality JSON report.
- Added dataset cleaning helpers.
- Added macro dataset validation helpers.
- Added column-name standardization.
- Added numeric-column coercion.
- Added rolling statistics.
- Added growth-rate calculation.
- Added z-score calculation.
- Added multi-line chart generation.
- Added scatter chart generation.
- Added real interest rate calculation.
- Added policy-rule benchmark interest rate calculation.
- Added full economic Markdown report.
- Added full analysis package generator.
- Added JSON diagnostics export.
- Added `quick_analyze` helper.
- Added public feature-list helper.
- Added professional command-line interface.

### CLI Added

The CLI now supports:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
python src/econkit_cli.py profile data/sample_economic_data.csv --output-dir outputs/profile
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
python src/econkit_cli.py cycle data/sample_economic_data.csv --output-dir outputs/cycle
python src/econkit_cli.py inflation data/sample_economic_data.csv --output-dir outputs/inflation
python src/econkit_cli.py mix data/sample_economic_data.csv --output-dir outputs/mix
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
python src/econkit_cli.py forecast data/sample_economic_data.csv --output-dir outputs/forecasts --periods 5
python src/econkit_cli.py ols data/sample_economic_data.csv --formula "inflation_rate ~ gdp_growth + unemployment_rate" --output-dir outputs/regression
python src/econkit_cli.py package data/sample_economic_data.csv --output-dir outputs/package --years 5
python src/econkit_cli.py features
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

### Documentation Added

- Added professional README.
- Added full CLI guide.
- Added expanded project structure documentation.
- Added installation instructions.
- Added Python API examples.
- Added command-line examples.
- Added troubleshooting guidance.
- Added limitations section.
- Added roadmap section.
- Added citation section.
- Added interpretation examples.

### Packaging Added

- Added professional `pyproject.toml`.
- Added package metadata.
- Added project keywords.
- Added Python version requirements.
- Added optional dependency groups:
  - `dev`
  - `excel`
  - `parquet`
  - `all`
- Added console script configuration:
  - `econkit = econkit_cli:main`
- Added pytest configuration.
- Added ruff configuration.

### Changed

- Reorganized EconKit around a more complete applied macroeconomic analysis workflow.
- Improved report generation.
- Improved CLI outputs.
- Improved compatibility with existing tests.
- Improved function naming consistency.
- Improved dataset cleaning behavior.
- Improved validation error messages.
- Improved documentation for command-line workflows.
- Improved project presentation for public GitHub use.

### Fixed

- Fixed business-cycle compatibility by supporting both:
  - `phase`
  - `business_cycle_phase`
- Fixed CLI backward compatibility for older helper functions.
- Fixed test stability around business-cycle outputs.
- Fixed earlier circular-import risk caused by accidental file misplacement.
- Stabilized GitHub Actions testing workflow.

### Notes

This release significantly expands EconKit from a beginner-friendly economics data analysis project into a broader applied macroeconomic toolkit.

The new tools are designed for:

- class projects
- research prototypes
- educational workflows
- policy memo drafts
- reproducible macroeconomic analysis
- early-stage applied economics projects

The macro risk, monetary policy, business-cycle, inflation, forecasting, and scenario tools remain transparent simplified models. They should not be interpreted as official forecasts or professional policy recommendations.

---

## [1.0.1] - Stability Release

### Added

- Added placeholder CLI test compatibility.
- Added stable test structure for GitHub Actions.
- Added improved release documentation.

### Changed

- Improved project reliability after CLI expansion.
- Improved test compatibility with existing project layout.

### Fixed

- Fixed stale CLI test import issue.
- Fixed failing GitHub Actions test caused by outdated test expectations.
- Fixed compatibility around removed or renamed CLI helper functions.

### Notes

This release focused on stabilizing the project after adding more CLI capabilities.

---

## [1.0.0] - First Public Stable Version

### Added

- Added initial EconKit project structure.
- Added core economic data analysis functions.
- Added summary statistics.
- Added average growth calculation.
- Added highest-value year finder.
- Added lowest-value year finder.
- Added correlation matrix calculation.
- Added line chart generation.
- Added basic report generation.
- Added macro risk analysis.
- Added monetary policy stance analysis.
- Added scenario simulation.
- Added command-line interface.
- Added sample dataset.
- Added GitHub Actions test workflow.
- Added README documentation.
- Added project requirements.
- Added tests.

### CLI Added

Initial CLI commands included:

```bash
python src/econkit_cli.py validate data/sample_economic_data.csv
python src/econkit_cli.py report data/sample_economic_data.csv --output-dir outputs/report
python src/econkit_cli.py risk data/sample_economic_data.csv --output-dir outputs/risk
python src/econkit_cli.py policy data/sample_economic_data.csv --output-dir outputs/policy
python src/econkit_cli.py scenarios data/sample_economic_data.csv --output-dir outputs/scenarios --years 5
python src/econkit_cli.py all data/sample_economic_data.csv --output-dir outputs --years 5
```

### Notes

This was the first stable public version of EconKit.

The goal of the release was to provide a beginner-friendly Python toolkit for economics data analysis and macroeconomic reporting.

---

## [0.3.0] - Macro Analysis Expansion

### Added

- Added macro risk classification.
- Added inflation pressure classification.
- Added growth condition classification.
- Added labor market classification.
- Added monetary condition classification.
- Added macro risk score.
- Added macro risk summary text.
- Added monetary policy stance analysis.
- Added simple policy-rule benchmark.
- Added policy gap calculation.
- Added monetary policy report generation.
- Added macro scenario simulation.
- Added default macro scenarios.
- Added scenario comparison.

### Changed

- Expanded EconKit from basic data analysis to macroeconomic interpretation.
- Improved report structure.
- Improved CLI scope.

### Notes

This version introduced the foundation for EconKit's macroeconomic diagnostics.

---

## [0.2.0] - Reporting and Visualization

### Added

- Added line chart generation.
- Added Markdown report generation.
- Added economic report workflow.
- Added output folder support.
- Added examples for report generation.

### Changed

- Improved beginner-friendly function names.
- Improved output readability.
- Improved project documentation.

### Notes

This release made EconKit more useful for students preparing class projects or simple analysis reports.

---

## [0.1.0] - Initial Prototype

### Added

- Added initial data loading examples.
- Added summary statistics.
- Added average value calculation.
- Added highest-value year finder.
- Added lowest-value year finder.
- Added correlation matrix calculation.
- Added sample economic dataset.
- Added basic tests.
- Added initial README.

### Notes

This was the first prototype of EconKit.

The original goal was to help economics students practice Python-based data analysis with clear, reusable examples.

---

# Release Philosophy

EconKit releases are designed around practical improvements.

A release is considered meaningful when it improves at least one of the following:

- data handling
- economic interpretation
- report generation
- reproducibility
- beginner usability
- command-line workflow
- testing reliability
- documentation quality
- public project professionalism

---

# Versioning Notes

EconKit version labels are used in a semantic-versioning style:

```text
MAJOR.MINOR.PATCH
```

General meaning:

| Version Type | Meaning |
|---|---|
| `MAJOR` | Large structural or compatibility-breaking changes |
| `MINOR` | New features added in a backward-compatible way |
| `PATCH` | Bug fixes, stability improvements, documentation corrections |

Because EconKit is still evolving, version numbers are practical project markers rather than strict package-distribution guarantees.

---

# Compatibility Notes

The current professional version aims to preserve compatibility with earlier project workflows.

Important compatibility choices:

- Older CLI helper names are preserved where possible.
- Business-cycle analysis supports both `phase` and `business_cycle_phase`.
- CLI commands can be run directly with `python src/econkit_cli.py`.
- Package installation is optional for direct local use.
- Tests use the `src` folder as the Python path.

---

# Educational Disclaimer

EconKit is designed for educational and exploratory economic analysis.

It is not:

- an official forecasting model
- a central-bank policy model
- a structural macroeconomic model
- a substitute for professional econometric software
- a source of investment advice
- a source of official policy recommendations

EconKit outputs should be used as transparent starting points for reasoning, discussion, and further analysis.
