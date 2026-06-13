"""Command-line interface for EconKit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from econkit import (
    analyze_business_cycle,
    analyze_macro_risk,
    analyze_monetary_policy_stance,
    generate_economic_report,
    generate_macro_scenario_analysis,
    load_economic_data,
    validate_macro_dataset,
)


def _write_json(data: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return output_path


def _write_markdown(title: str, analysis: dict, summary_key: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", "This file was automatically generated with EconKit.", ""]

    for key, value in analysis.items():
        if isinstance(value, dict):
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            for child_key, child_value in value.items():
                lines.append(f"- {child_key.replace('_', ' ').title()}: {child_value}")
            lines.append("")
        elif key != summary_key:
            lines.append(f"- {key.replace('_', ' ').title()}: {value}")

    if summary_key in analysis:
        lines.extend(["", "## Summary", "", analysis[summary_key]])

    lines.extend(
        [
            "",
            "## Educational note",
            "",
            "This output is for educational analysis and should not be interpreted as professional forecasting or official policy advice.",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def command_validate(args: argparse.Namespace) -> None:
    data = load_economic_data(args.data_path)
    validate_macro_dataset(data)
    print("Dataset validation passed.")
    print(f"Rows: {len(data)}")
    print(f"Columns: {', '.join(data.columns)}")


def command_report(args: argparse.Namespace) -> None:
    report_path = generate_economic_report(args.data_path, args.output_dir)
    print("Economic report generated successfully.")
    print(f"Report saved to: {report_path}")


def command_risk(args: argparse.Namespace) -> None:
    data = load_economic_data(args.data_path)
    validate_macro_dataset(data)
    analysis = analyze_macro_risk(data)
    output_dir = Path(args.output_dir)

    markdown_path = _write_markdown("Macro Risk Summary", analysis, "summary", output_dir / "macro_risk_summary.md")
    json_path = _write_json(analysis, output_dir / "macro_risk_summary.json")

    print("Macro risk analysis completed.")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")
    print(f"Overall macro risk: {analysis['overall_risk']}")


def command_policy(args: argparse.Namespace) -> None:
    data = load_economic_data(args.data_path)
    validate_macro_dataset(data)
    analysis = analyze_monetary_policy_stance(
        data,
        target_inflation=args.target_inflation,
        neutral_interest_rate=args.neutral_interest_rate,
        potential_growth=args.potential_growth,
        inflation_weight=args.inflation_weight,
        growth_weight=args.growth_weight,
    )
    output_dir = Path(args.output_dir)

    markdown_path = _write_markdown(
        "Monetary Policy Stance Summary",
        analysis,
        "summary",
        output_dir / "monetary_policy_summary.md",
    )
    json_path = _write_json(analysis, output_dir / "monetary_policy_summary.json")

    print("Monetary policy stance analysis completed.")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")
    print(f"Policy stance: {analysis['policy_stance']}")
    print(f"Policy gap: {analysis['policy_gap']:.2f}")


def command_cycle(args: argparse.Namespace) -> None:
    data = load_economic_data(args.data_path)
    validate_macro_dataset(data)
    analysis = analyze_business_cycle(data)
    output_dir = Path(args.output_dir)

    markdown_path = _write_markdown(
        "Business Cycle Diagnosis",
        analysis,
        "summary",
        output_dir / "business_cycle_summary.md",
    )
    json_path = _write_json(analysis, output_dir / "business_cycle_summary.json")

    print("Business cycle diagnosis completed.")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")
    print(f"Business-cycle phase: {analysis['business_cycle_phase']}")


def command_scenarios(args: argparse.Namespace) -> None:
    results = generate_macro_scenario_analysis(
        data_path=args.data_path,
        output_dir=args.output_dir,
        years=args.years,
    )
    print("Macro scenario analysis completed.")
    print(f"Scenario comparison saved to: {results['comparison_path']}")
    print(f"Scenario report saved to: {results['report_path']}")
    print("Generated scenario files:")
    for scenario_name, scenario_path in results["scenario_paths"].items():
        print(f"- {scenario_name}: {scenario_path}")


def command_all(args: argparse.Namespace) -> None:
    data = load_economic_data(args.data_path)
    validate_macro_dataset(data)

    output_dir = Path(args.output_dir)
    report_path = generate_economic_report(args.data_path, output_dir / "report")

    risk_analysis = analyze_macro_risk(data)
    _write_markdown("Macro Risk Summary", risk_analysis, "summary", output_dir / "risk" / "macro_risk_summary.md")
    _write_json(risk_analysis, output_dir / "risk" / "macro_risk_summary.json")

    policy_analysis = analyze_monetary_policy_stance(data)
    _write_markdown(
        "Monetary Policy Stance Summary",
        policy_analysis,
        "summary",
        output_dir / "policy" / "monetary_policy_summary.md",
    )
    _write_json(policy_analysis, output_dir / "policy" / "monetary_policy_summary.json")

    cycle_analysis = analyze_business_cycle(data)
    _write_markdown(
        "Business Cycle Diagnosis",
        cycle_analysis,
        "summary",
        output_dir / "cycle" / "business_cycle_summary.md",
    )
    _write_json(cycle_analysis, output_dir / "cycle" / "business_cycle_summary.json")

    scenario_results = generate_macro_scenario_analysis(
        data_path=args.data_path,
        output_dir=output_dir / "scenarios",
        years=args.years,
    )

    print("EconKit full analysis completed.")
    print(f"Economic report: {report_path}")
    print(f"Scenario report: {scenario_results['report_path']}")
    print(f"Overall macro risk: {risk_analysis['overall_risk']}")
    print(f"Policy stance: {policy_analysis['policy_stance']}")
    print(f"Business-cycle phase: {cycle_analysis['business_cycle_phase']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "EconKit: beginner-friendly economics data analysis, reporting, macro risk, "
            "monetary policy stance, business-cycle diagnosis, and scenario simulation."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate an economic CSV dataset.")
    validate_parser.add_argument("data_path")
    validate_parser.set_defaults(func=command_validate)

    report_parser = subparsers.add_parser("report", help="Generate an economic report and charts.")
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

    cycle_parser = subparsers.add_parser("cycle", help="Diagnose the business-cycle phase.")
    cycle_parser.add_argument("data_path")
    cycle_parser.add_argument("--output-dir", default="outputs/cycle")
    cycle_parser.set_defaults(func=command_cycle)

    scenarios_parser = subparsers.add_parser("scenarios", help="Generate macroeconomic scenario simulations.")
    scenarios_parser.add_argument("data_path")
    scenarios_parser.add_argument("--output-dir", default="outputs/scenarios")
    scenarios_parser.add_argument("--years", type=int, default=5)
    scenarios_parser.set_defaults(func=command_scenarios)

    all_parser = subparsers.add_parser("all", help="Run the full EconKit analysis pipeline.")
    all_parser.add_argument("data_path")
    all_parser.add_argument("--output-dir", default="outputs")
    all_parser.add_argument("--years", type=int, default=5)
    all_parser.set_defaults(func=command_all)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


def run_cli() -> None:
    main()


if __name__ == "__main__":
    main()
