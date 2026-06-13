import argparse
from pathlib import Path

from econkit import analyze_macro_risk, generate_economic_report, load_economic_data


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


def run_cli():
    """
    Run the EconKit command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Generate beginner-friendly economic analysis reports."
    )

    parser.add_argument(
        "data_path",
        help="Path to the economic CSV dataset."
    )

    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory where generated reports and charts will be saved."
    )

    args = parser.parse_args()

    data_path = Path(args.data_path)
    output_dir = Path(args.output_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    print("Running EconKit analysis...")
    print(f"Dataset: {data_path}")
    print(f"Output directory: {output_dir}")
    print()

    report_path = generate_economic_report(data_path, output_dir)

    data = load_economic_data(data_path)
    macro_risk_analysis = analyze_macro_risk(data)
    risk_summary_path = save_macro_risk_summary(macro_risk_analysis, output_dir)

    print("Analysis completed successfully.")
    print(f"Economic report: {report_path}")
    print(f"Macro risk summary: {risk_summary_path}")
    print()
    print("Overall macro risk:", macro_risk_analysis["overall_risk"])
    print("Summary:", macro_risk_analysis["summary"])


if __name__ == "__main__":
    run_cli()
