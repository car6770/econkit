import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import generate_macro_scenario_analysis


if __name__ == "__main__":
    data_path = project_root / "data" / "sample_economic_data.csv"
    output_dir = project_root / "outputs" / "scenarios"

    results = generate_macro_scenario_analysis(
        data_path=data_path,
        output_dir=output_dir,
        years=5,
    )

    print("Macro scenario analysis completed.")
    print(f"Scenario comparison saved to: {results['comparison_path']}")
    print(f"Scenario report saved to: {results['report_path']}")
    print()
    print("Generated scenario files:")

    for scenario_name, scenario_path in results["scenario_paths"].items():
        print(f"- {scenario_name}: {scenario_path}")
