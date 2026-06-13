import argparse
import json
from pathlib import Path

from econkit import (
    analyze_macro_risk,
    analyze_monetary_policy_stance,
    generate_economic_report,
    generate_macro_scenario_analysis,
    load_economic_data,
)


REQUIRED_COLUMNS = [
    "year",
    "gdp_growth",
    "inflation_rate",
    "unemployment_rate",
    "interest_rate",
]


def validate_dataset(data):
    """
    Validate that the dataset includes the required macroeconomic columns.
    """
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if data.empty:
        raise ValueError("Dataset is empty.")

    return True


def save_macro_risk_summary(analysis, output_dir):
    """
    Save macro risk analysis results as a Markdown file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "macro_risk_summary.md"

    lines = []
    lines.append("# Macro Risk Summary")
    lines.append("")
    lines.append(f"- Latest year: {analysis['latest_year']}")
    lines.append(f"- Risk score: {analysis['risk_score']}")
    lines.append(f"- Overall risk: {analysis['overall_risk']}")
    lines.append("")
    lines.append("## Signals")
    lines.append("")

    for signal_name, signal_value in analysis["signals"].items():
        readable_name = signal_name.replace("_", " ").title()
        lines.append(f"- {readable_name}: {signal_value}")

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(analysis["summary"])
    lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append(
        "This analysis is intended for educational use and should not be interpreted "
        "as a formal forecast or professional economic assessment."
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def save_macro_risk_json(analysis, output_dir):
    """
    Save macro risk analysis results as a JSON file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "macro_risk_summary.json"

    output_path.write_text(
        json.dumps(analysis, indent=2),
        encoding="utf-8",
    )

    return output_path


def save_monetary_policy_summary(analysis, output_dir):
    """
    Save monetary policy stance analysis results as a Markdown file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "monetary_policy_summary.md"

    lines = []
    lines.append("# Monetary Policy Stance Summary")
    lines.append("")
    lines.append(f"- Latest year: {analysis['latest_year']}")
    lines.append(f"- Policy stance: {analysis['policy_stance']}")
    lines.append(f"- Actual interest rate: {analysis['actual_interest_rate']:.2f}")
    lines.append(
        f"- Recommended policy-rule rate: "
        f"{analysis['recommended_policy_rate']:.2f}"
    )
    lines.append(f"- Policy gap: {analysis['policy_gap']:.2f}")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")

    for input_name, input_value in analysis["inputs"].items():
        readable_name = input_name.replace("_", " ").title()
        lines.append(f"- {readable_name}: {input_value:.2f}")

    lines.append("")
    lines.append("## Economic gaps")
    lines.append("")

    for gap_name, gap_value in analysis["gaps"].items():
        readable_name = gap_name.replace("_", " ").title()
        lines.append(f"- {readable_name}: {gap_value:.2f}")

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(analysis["summary"])
    lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append(
        "This monetary policy analysis is a simplified educational tool. "
        "It should not be interpreted as an official policy recommendation."
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def save_monetary_policy_json(analysis, output_dir):
    """
    Save monetary policy stance analysis results as a JSON file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "monetary_policy_summary.json"

    output_path.write_text(
        json.dumps(analysis, indent=2),
        encoding="utf-8",
    )

    return output_path


def command_validate(args):
    """
    Validate an economic dataset.
    """
    data = load_economic_data(args.data_path)
    validate_dataset(data)

    print("Dataset validation passed.")
    print(f"Rows: {len(data)}")
    print(f"Columns: {', '.join(data.columns)}")


def command_report(args):
    """
    Generate an economic report and charts.
    """
    data = load_economic_data(args.data_path)
    validate_dataset(data)

    report_path = generate_economic_report(args.data_path, args.output_dir)

    print("Economic report generated successfully.")
    print(f"Report saved to: {report_path}")


def command_risk(args):
    """
    Generate macro risk analysis outputs.
    """
    data = load_economic_data(args.data_path)
    validate_dataset(data)

    analysis = analyze_macro_risk(data)

    markdown_path = save_macro_risk_summary(analysis, args.output_dir)
    json_path = save_macro_risk_json(analysis, args.output_dir)

    print("Macro risk analysis completed.")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")
    print(f"Overall macro risk: {analysis['overall_risk']}")


def command_policy(args):
    """
    Generate monetary policy stance analysis outputs.
    """
    data = load_economic_data(args.data_path)
    validate_dataset(data)

    analysis = analyze_monetary_policy_stance(
        data,
        target_inflation=args.target_inflation,
        neutral_interest_rate=args.neutral_interest_rate,
        potential_growth=args.potential_growth,
    )

    markdown_path = save_monetary_policy_summary(analysis, args.output_dir)
    json_path = save_monetary_policy_json(analysis, args.output_dir)

    print("Monetary policy stance analysis completed.")
    print(f"Markdown summary saved to: {markdown_path}")
    print(f"JSON summary saved to: {json_path}")
    print(f"Policy stance: {analysis['policy_stance']}")
    print(f"Actual interest rate: {analysis['actual_interest_rate']:.2f}")
    print(f"Recommended policy-rule rate: {analysis['recommended_policy_rate']:.2f}")
    print(f"Policy gap: {analysis['policy_gap']:.2f}")


def command_scenarios(args):
    """
    Generate macro scenario simulation outputs.
    """
    data = load_economic_data(args.data_path)
    validate_dataset(data)

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


def command_all(args):
    """
    Run the full EconKit analysis pipeline.
    """
    data = load_economic_data(args.data_path)
    validate_dataset(data)

    output_dir = Path(args.output_dir)

    report_dir = output_dir / "report"
    risk_dir = output_dir / "risk"
    policy_dir = output_dir / "policy"
    scenario_dir = output_dir / "scenarios"

    report_path = generate_economic_report(args.data_path, report_dir)

    risk_analysis = analyze_macro_risk(data)
    risk_markdown_path = save_macro_risk_summary(risk_analysis, risk_dir)
    risk_json_path = save_macro_risk_json(risk_analysis, risk_dir)

    policy_analysis = analyze_monetary_policy_stance(data)
    policy_markdown_path = save_monetary_policy_summary(
        policy_analysis,
        policy_dir,
    )
    policy_json_path = save_monetary_policy_json(
        policy_analysis,
        policy_dir,
    )

    scenario_results = generate_macro_scenario_analysis(
        data_path=args.data_path,
        output_dir=scenario_dir,
        years=args.years,
    )

    print("EconKit full analysis completed.")
    print("")
    print("Generated outputs:")
    print(f"- Economic report: {report_path}")
    print(f"- Macro risk Markdown summary: {risk_markdown_path}")
    print(f"- Macro risk JSON summary: {risk_json_path}")
    print(f"- Monetary policy Markdown summary: {policy_markdown_path}")
    print(f"- Monetary policy JSON summary: {policy_json_path}")
    print(f"- Scenario comparison: {scenario_results['comparison_path']}")
    print(f"- Scenario report: {scenario_results['report_path']}")
    print("")
    print(f"Overall macro risk: {risk_analysis['overall_risk']}")
    print(f"Policy stance: {policy_analysis['policy_stance']}")
    print(f"Macro summary: {risk_analysis['summary']}")
    print(f"Policy summary: {policy_analysis['summary']}")


def build_parser():
    """
    Build the EconKit command-line parser.
    """
    parser = argparse.ArgumentParser(
        description=(
            "EconKit: beginner-friendly economics data analysis, reporting, "
            "macro risk analysis, monetary policy analysis, and scenario simulation."
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate an economic CSV dataset.",
    )
    validate_parser.add_argument("data_path")
    validate_parser.set_defaults(func=command_validate)

    report_parser = subparsers.add_parser(
        "report",
        help="Generate an economic report and charts.",
    )
    report_parser.add_argument("data_path")
    report_parser.add_argument(
        "--output-dir",
        default="outputs/report",
        help="Directory where report outputs will be saved.",
    )
    report_parser.set_defaults(func=command_report)

    risk_parser = subparsers.add_parser(
        "risk",
        help="Generate macro risk analysis outputs.",
    )
    risk_parser.add_argument("data_path")
    risk_parser.add_argument(
        "--output-dir",
        default="outputs/risk",
        help="Directory where risk outputs will be saved.",
    )
    risk_parser.set_defaults(func=command_risk)

    policy_parser = subparsers.add_parser(
        "policy",
        help="Analyze monetary policy stance.",
    )
    policy_parser.add_argument("data_path")
    policy_parser.add_argument(
        "--output-dir",
        default="outputs/policy",
        help="Directory where monetary policy outputs will be saved.",
    )
    policy_parser.add_argument(
        "--target-inflation",
        type=float,
        default=2.0,
        help="Inflation target used in the simple policy rule.",
    )
    policy_parser.add_argument(
        "--neutral-interest-rate",
        type=float,
        default=None,
        help=(
            "Neutral interest rate used in the simple policy rule. "
            "If omitted, EconKit uses a recent historical average."
        ),
    )
    policy_parser.add_argument(
        "--potential-growth",
        type=float,
        default=None,
        help=(
            "Potential growth rate used in the simple policy rule. "
            "If omitted, EconKit uses a recent historical average."
        ),
    )
    policy_parser.set_defaults(func=command_policy)

    scenarios_parser = subparsers.add_parser(
        "scenarios",
        help="Generate macroeconomic scenario simulation outputs.",
    )
    scenarios_parser.add_argument("data_path")
    scenarios_parser.add_argument(
        "--output-dir",
        default="outputs/scenarios",
        help="Directory where scenario outputs will be saved.",
    )
    scenarios_parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="Number of future years to simulate.",
    )
    scenarios_parser.set_defaults(func=command_scenarios)

    all_parser = subparsers.add_parser(
        "all",
        help="Run the full EconKit analysis pipeline.",
    )
    all_parser.add_argument("data_path")
    all_parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory where all outputs will be saved.",
    )
    all_parser.add_argument(
        "--years",
        type=int,
        default=5,
        help="Number of future years to simulate.",
    )
    all_parser.set_defaults(func=command_all)

    return parser


def run_cli():
    """
    Run the EconKit command-line interface.
    """
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    run_cli()
