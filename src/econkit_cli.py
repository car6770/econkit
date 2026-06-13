"""
EconKit Command-Line Interface
==============================

Upload this file to:

    src/econkit_cli.py

This CLI is compatible with the current EconKit core engine and keeps older
helper functions such as save_macro_risk_summary for backward compatibility.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Optional

from econkit import (
    DEFAULT_INDICATORS,
    analyze_business_cycle,
    analyze_inflation_pressure,
    analyze_macro_risk,
    analyze_monetary_policy_stance,
    analyze_policy_mix,
    clean_macro_dataset,
    data_quality_report,
    generate_economic_report,
    generate_forecast_table,
    generate_full_analysis_package,
    generate_macro_scenario_analysis,
    generate_monetary_policy_report,
    list_available_features,
    load_economic_data,
    profile_dataset,
    regression_report,
    run_ols_formula,
    validate_macro_dataset,
)


def _ensure_output_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _load_clean_validate(data_path: str | Path):
    data = load_economic_data(data_path)
    data = clean_macro_dataset(data)
    validate_macro_dataset(data)
    return data


def _write_json(payload: Mapping[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def _write_markdown(title: str, sections: Mapping[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# {title}", ""]

    for section_title, section_value in sections.items():
        lines.append(f"## {section_title}")
        lines.append("")

        if isinstance(section_value, dict):
            for key, value in section_value.items():
                readable_key = str(key).replace("_", " ").title()
                if isinstance(value, (dict, list)):
                    lines.append(f"- **{readable_key}:** `{json.dumps(value, default=str)}`")
                else:
                    lines.append(f"- **{readable_key}:** {value}")
        elif isinstance(section_value, list):
            for item in section_value:
                lines.append(f"- {item}")
        else:
            lines.append(str(section_value))

        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Backward-compatible helper functions
# ---------------------------------------------------------------------------


def validate_dataset(data):
    """
    Backward-compatible dataset validator.

    Older examples/tests imported this function from econkit_cli.py.
    """
    return validate_macro_dataset(data)


def save_macro_risk_summary(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """
    Save macro risk analysis as Markdown.

    Kept for backward compatibility with earlier EconKit versions.
    """
    output_dir = _ensure_output_dir(output_dir)
    output_path = output_dir / "macro_risk_summary.md"

    sections = {
        "Overview": {
            "latest_year": analysis.get("latest_year"),
            "risk_score": analysis.get("risk_score"),
            "overall_risk": analysis.get("overall_risk"),
        },
        "Signals": analysis.get("signals", {}),
        "Summary": analysis.get("summary", ""),
        "Note": (
            "This analysis is intended for educational and exploratory use. "
            "It should not be interpreted as a formal forecast."
        ),
    }

    return _write_markdown("Macro Risk Summary", sections, output_path)


def save_macro_risk_json(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """
    Save macro risk analysis as JSON.

    Kept for backward compatibility with earlier EconKit versions.
    """
    output_dir = _ensure_output_dir(output_dir)
    return _write_json(analysis, output_dir / "macro_risk_summary.json")


def save_monetary_policy_summary(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """Save monetary policy stance analysis as Markdown."""
    output_dir = _ensure_output_dir(output_dir)
    output_path = output_dir / "monetary_policy_summary.md"

    sections = {
        "Overview": {
            "latest_year": analysis.get("latest_year"),
            "policy_stance": analysis.get("policy_stance"),
            "actual_interest_rate": analysis.get("actual_interest_rate"),
            "recommended_policy_rate": analysis.get("recommended_policy_rate"),
            "policy_gap": analysis.get("policy_gap"),
            "real_interest_rate": analysis.get("real_interest_rate"),
        },
        "Inputs": analysis.get("inputs", {}),
        "Gaps": analysis.get("gaps", {}),
        "Summary": analysis.get("summary", ""),
        "Note": (
            "This analysis uses a transparent simplified policy-rule benchmark. "
            "It is not an official policy recommendation."
        ),
    }

    return _write_markdown("Monetary Policy Stance Summary", sections, output_path)


def save_monetary_policy_json(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """Save monetary policy stance analysis as JSON."""
    output_dir = _ensure_output_dir(output_dir)
    return _write_json(analysis, output_dir / "monetary_policy_summary.json")


def save_business_cycle_summary(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """Save business-cycle diagnosis as Markdown."""
    output_dir = _ensure_output_dir(output_dir)
    output_path = output_dir / "business_cycle_summary.md"

    sections = {
        "Overview": {
            "latest_year": analysis.get("latest_year"),
            "phase": analysis.get("business_cycle_phase", analysis.get("phase")),
            "gdp_growth": analysis.get("gdp_growth"),
            "estimated_potential_growth": analysis.get("estimated_potential_growth"),
            "output_gap_proxy": analysis.get("output_gap_proxy"),
        },
        "Summary": analysis.get("summary", ""),
    }

    return _write_markdown("Business Cycle Summary", sections, output_path)


def save_inflation_summary(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """Save inflation pressure diagnosis as Markdown."""
    output_dir = _ensure_output_dir(output_dir)
    output_path = output_dir / "inflation_pressure_summary.md"

    sections = {
        "Overview": {
            "latest_year": analysis.get("latest_year"),
            "inflation_rate": analysis.get("inflation_rate"),
            "target_inflation": analysis.get("target_inflation"),
            "inflation_gap": analysis.get("inflation_gap"),
            "pressure": analysis.get("pressure"),
            "momentum_label": analysis.get("momentum_label"),
        },
        "Summary": analysis.get("summary", ""),
    }

    return _write_markdown("Inflation Pressure Summary", sections, output_path)


def save_policy_mix_summary(analysis: Mapping[str, Any], output_dir: str | Path) -> Path:
    """Save policy-mix diagnosis as Markdown."""
    output_dir = _ensure_output_dir(output_dir)
    output_path = output_dir / "policy_mix_summary.md"

    sections = {
        "Overview": {
            "regime": analysis.get("regime"),
            "score": analysis.get("score"),
        },
        "Summary": analysis.get("summary", ""),
    }

    return _write_markdown("Policy Mix Summary", sections, output_path)


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def command_validate(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)

    print("Dataset validation passed.")
    print(f"Rows: {len(data)}")
    print(f"Columns: {', '.join(data.columns)}")


def command_profile(args: argparse.Namespace) -> None:
    data = load_economic_data(args.data_path)
    data = clean_macro_dataset(data)

    output_dir = _ensure_output_dir(args.output_dir)
    profile = profile_dataset(data)
    report_dict = data_quality_report(data, output_dir / "data_quality_report.md")
    json_path = _write_json(report_dict, output_dir / "data_quality_report.json")

    print("Data-quality profile created.")
    print(f"Rows: {profile.rows}")
    print(f"Columns: {profile.columns}")
    print(f"Markdown report saved to: {output_dir / 'data_quality_report.md'}")
    print(f"JSON report saved to: {json_path}")


def command_report(args: argparse.Namespace) -> None:
    report_path = generate_economic_report(args.data_path, args.output_dir)

    print("Economic report generated successfully.")
    print(f"Report saved to: {report_path}")


def command_risk(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    analysis = analyze_macro_risk(data)
    markdown_path = save_macro_risk_summary(analysis, output_dir)
    json_path = save_macro_risk_json(analysis, output_dir)

    print("Macro risk analysis completed.")
    print(f"Overall macro risk: {analysis['overall_risk']}")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")


def command_policy(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    analysis = analyze_monetary_policy_stance(
        data,
        target_inflation=args.target_inflation,
        neutral_interest_rate=args.neutral_interest_rate,
        potential_growth=args.potential_growth,
        inflation_weight=args.inflation_weight,
        growth_weight=args.growth_weight,
    )

    markdown_path = save_monetary_policy_summary(analysis, output_dir)
    json_path = save_monetary_policy_json(analysis, output_dir)
    full_report_path = generate_monetary_policy_report(data, output_dir / "monetary_policy_report.md")

    print("Monetary policy stance analysis completed.")
    print(f"Policy stance: {analysis['policy_stance']}")
    print(f"Policy gap: {analysis['policy_gap']:.2f}")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")
    print(f"Full report saved to: {full_report_path}")


def command_cycle(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    analysis = analyze_business_cycle(data)
    markdown_path = save_business_cycle_summary(analysis, output_dir)
    json_path = _write_json(analysis, output_dir / "business_cycle_summary.json")

    phase = analysis.get("business_cycle_phase", analysis.get("phase"))

    print("Business-cycle diagnosis completed.")
    print(f"Business-cycle phase: {phase}")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")


def command_inflation(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    analysis = analyze_inflation_pressure(
        data,
        target_inflation=args.target_inflation,
        window=args.window,
    )
    markdown_path = save_inflation_summary(analysis, output_dir)
    json_path = _write_json(analysis, output_dir / "inflation_pressure_summary.json")

    print("Inflation pressure diagnosis completed.")
    print(f"Inflation pressure: {analysis['pressure']}")
    print(f"Inflation momentum: {analysis['momentum_label']}")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")


def command_mix(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    analysis = analyze_policy_mix(data)
    markdown_path = save_policy_mix_summary(analysis, output_dir)
    json_path = _write_json(analysis, output_dir / "policy_mix_summary.json")

    print("Policy-mix analysis completed.")
    print(f"Regime: {analysis['regime']}")
    print(f"Score: {analysis['score']}")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")


def command_scenarios(args: argparse.Namespace) -> None:
    results = generate_macro_scenario_analysis(
        data_path=args.data_path,
        output_dir=args.output_dir,
        years=args.years,
        stress_tests=args.stress_tests,
    )

    print("Macro scenario analysis completed.")
    print(f"Scenario comparison saved to: {results['comparison_path']}")
    print(f"Scenario report saved to: {results['report_path']}")
    print("Generated scenario files:")

    for scenario_name, scenario_path in results["scenario_paths"].items():
        print(f"- {scenario_name}: {scenario_path}")


def command_forecast(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    columns = args.columns if args.columns else DEFAULT_INDICATORS
    forecasts = generate_forecast_table(
        data,
        columns=columns,
        periods=args.periods,
        method=args.method,
    )

    output_path = output_dir / "indicator_forecasts.csv"
    forecasts.to_csv(output_path, index=False)

    print("Forecast table generated.")
    print(f"Forecasts saved to: {output_path}")
    print(f"Rows: {len(forecasts)}")


def command_ols(args: argparse.Namespace) -> None:
    data = _load_clean_validate(args.data_path)
    output_dir = _ensure_output_dir(args.output_dir)

    result = run_ols_formula(
        data,
        formula=args.formula,
        robust=args.robust,
    )

    report_path = output_dir / "regression_report.md"
    json_path = output_dir / "regression_result.json"

    regression_report(result, report_path)
    _write_json(result.to_dict(), json_path)

    print("OLS regression completed.")
    print(f"Formula: {args.formula}")
    print(f"R-squared: {result.r_squared:.4f}")
    print(f"Report saved to: {report_path}")
    print(f"JSON result saved to: {json_path}")


def command_package(args: argparse.Namespace) -> None:
    results = generate_full_analysis_package(
        data_path=args.data_path,
        output_dir=args.output_dir,
        years=args.years,
    )

    print("Full EconKit analysis package generated.")
    print(f"Cleaned data: {results['cleaned_data_path']}")
    print(f"Economic report: {results['report_path']}")
    print(f"Policy report: {results['policy_report_path']}")
    print(f"Forecasts: {results['forecast_path']}")
    print(f"Diagnostics: {results['diagnostics_path']}")
    print(f"Scenario report: {results['scenario_results']['report_path']}")


def command_features(args: argparse.Namespace) -> None:
    print("Available EconKit features:")
    for feature in list_available_features():
        print(f"- {feature}")


def command_all(args: argparse.Namespace) -> None:
    output_dir = _ensure_output_dir(args.output_dir)

    data = _load_clean_validate(args.data_path)

    report_dir = output_dir / "report"
    risk_dir = output_dir / "risk"
    policy_dir = output_dir / "policy"
    cycle_dir = output_dir / "cycle"
    inflation_dir = output_dir / "inflation"
    mix_dir = output_dir / "mix"
    scenario_dir = output_dir / "scenarios"
    forecast_dir = output_dir / "forecasts"

    report_path = generate_economic_report(args.data_path, report_dir)

    risk_analysis = analyze_macro_risk(data)
    save_macro_risk_summary(risk_analysis, risk_dir)
    save_macro_risk_json(risk_analysis, risk_dir)

    policy_analysis = analyze_monetary_policy_stance(data)
    save_monetary_policy_summary(policy_analysis, policy_dir)
    save_monetary_policy_json(policy_analysis, policy_dir)

    cycle_analysis = analyze_business_cycle(data)
    save_business_cycle_summary(cycle_analysis, cycle_dir)
    _write_json(cycle_analysis, cycle_dir / "business_cycle_summary.json")

    inflation_analysis = analyze_inflation_pressure(data)
    save_inflation_summary(inflation_analysis, inflation_dir)
    _write_json(inflation_analysis, inflation_dir / "inflation_pressure_summary.json")

    mix_analysis = analyze_policy_mix(data)
    save_policy_mix_summary(mix_analysis, mix_dir)
    _write_json(mix_analysis, mix_dir / "policy_mix_summary.json")

    scenario_results = generate_macro_scenario_analysis(
        data_path=args.data_path,
        output_dir=scenario_dir,
        years=args.years,
        stress_tests=args.stress_tests,
    )

    forecasts = generate_forecast_table(data, DEFAULT_INDICATORS, periods=args.years)
    forecast_dir.mkdir(parents=True, exist_ok=True)
    forecast_path = forecast_dir / "indicator_forecasts.csv"
    forecasts.to_csv(forecast_path, index=False)

    print("EconKit full analysis completed.")
    print("")
    print("Generated outputs:")
    print(f"- Economic report: {report_path}")
    print(f"- Macro risk: {risk_dir}")
    print(f"- Monetary policy: {policy_dir}")
    print(f"- Business cycle: {cycle_dir}")
    print(f"- Inflation pressure: {inflation_dir}")
    print(f"- Policy mix: {mix_dir}")
    print(f"- Scenario report: {scenario_results['report_path']}")
    print(f"- Forecast table: {forecast_path}")
    print("")
    print(f"Overall macro risk: {risk_analysis['overall_risk']}")
    print(f"Policy stance: {policy_analysis['policy_stance']}")
    print(f"Policy-mix regime: {mix_analysis['regime']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="econkit",
        description=(
            "EconKit: economics data analysis, reporting, macro diagnostics, "
            "scenario simulation, forecasting, and lightweight econometrics."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a macroeconomic dataset.")
    validate_parser.add_argument("data_path")
    validate_parser.set_defaults(func=command_validate)

    profile_parser = subparsers.add_parser("profile", help="Create a data-quality profile.")
    profile_parser.add_argument("data_path")
    profile_parser.add_argument("--output-dir", default="outputs/profile")
    profile_parser.set_defaults(func=command_profile)

    report_parser = subparsers.add_parser("report", help="Generate charts and an economic report.")
    report_parser.add_argument("data_path")
    report_parser.add_argument("--output-dir", default="outputs/report")
    report_parser.set_defaults(func=command_report)

    risk_parser = subparsers.add_parser("risk", help="Analyze macroeconomic risk.")
    risk_parser.add_argument("data_path")
    risk_parser.add_argument("--output-dir", default="outputs/risk")
    risk_parser.set_defaults(func=command_risk)

    policy_parser = subparsers.add_parser("policy", help="Analyze monetary policy stance.")
    policy_parser.add_argument("data_path")
    policy_parser.add_argument("--output-dir", default="outputs/policy")
    policy_parser.add_argument("--target-inflation", type=float, default=2.0)
    policy_parser.add_argument("--neutral-interest-rate", type=float, default=None)
    policy_parser.add_argument("--potential-growth", type=float, default=None)
    policy_parser.add_argument("--inflation-weight", type=float, default=0.5)
    policy_parser.add_argument("--growth-weight", type=float, default=0.5)
    policy_parser.set_defaults(func=command_policy)

    cycle_parser = subparsers.add_parser("cycle", help="Diagnose business-cycle conditions.")
    cycle_parser.add_argument("data_path")
    cycle_parser.add_argument("--output-dir", default="outputs/cycle")
    cycle_parser.set_defaults(func=command_cycle)

    inflation_parser = subparsers.add_parser("inflation", help="Diagnose inflation pressure.")
    inflation_parser.add_argument("data_path")
    inflation_parser.add_argument("--output-dir", default="outputs/inflation")
    inflation_parser.add_argument("--target-inflation", type=float, default=2.0)
    inflation_parser.add_argument("--window", type=int, default=3)
    inflation_parser.set_defaults(func=command_inflation)

    mix_parser = subparsers.add_parser("mix", help="Analyze the macro policy mix.")
    mix_parser.add_argument("data_path")
    mix_parser.add_argument("--output-dir", default="outputs/mix")
    mix_parser.set_defaults(func=command_mix)

    scenarios_parser = subparsers.add_parser("scenarios", help="Generate macro scenario simulations.")
    scenarios_parser.add_argument("data_path")
    scenarios_parser.add_argument("--output-dir", default="outputs/scenarios")
    scenarios_parser.add_argument("--years", type=int, default=5)
    scenarios_parser.add_argument("--stress-tests", action="store_true")
    scenarios_parser.set_defaults(func=command_scenarios)

    forecast_parser = subparsers.add_parser("forecast", help="Generate indicator forecasts.")
    forecast_parser.add_argument("data_path")
    forecast_parser.add_argument("--output-dir", default="outputs/forecasts")
    forecast_parser.add_argument("--periods", type=int, default=5)
    forecast_parser.add_argument("--method", choices=["ar1", "moving_average"], default="ar1")
    forecast_parser.add_argument("--columns", nargs="*", default=None)
    forecast_parser.set_defaults(func=command_forecast)

    ols_parser = subparsers.add_parser("ols", help="Run lightweight OLS regression.")
    ols_parser.add_argument("data_path")
    ols_parser.add_argument("--formula", required=True, help="Example: 'inflation_rate ~ gdp_growth + unemployment_rate'")
    ols_parser.add_argument("--output-dir", default="outputs/regression")
    ols_parser.add_argument("--robust", action="store_true", help="Use White robust standard errors.")
    ols_parser.set_defaults(func=command_ols)

    package_parser = subparsers.add_parser("package", help="Generate a full analysis package.")
    package_parser.add_argument("data_path")
    package_parser.add_argument("--output-dir", default="outputs/package")
    package_parser.add_argument("--years", type=int, default=5)
    package_parser.set_defaults(func=command_package)

    features_parser = subparsers.add_parser("features", help="List available EconKit features.")
    features_parser.set_defaults(func=command_features)

    all_parser = subparsers.add_parser("all", help="Run the main EconKit analysis workflow.")
    all_parser.add_argument("data_path")
    all_parser.add_argument("--output-dir", default="outputs")
    all_parser.add_argument("--years", type=int, default=5)
    all_parser.add_argument("--stress-tests", action="store_true")
    all_parser.set_defaults(func=command_all)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


def run_cli() -> None:
    main()


if __name__ == "__main__":
    main()
