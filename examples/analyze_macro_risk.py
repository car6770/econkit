import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import analyze_macro_risk, load_economic_data


if __name__ == "__main__":
    data_path = project_root / "data" / "sample_economic_data.csv"
    data = load_economic_data(data_path)

    analysis = analyze_macro_risk(data)

    print("Macro Risk Analysis")
    print("===================")
    print(f"Latest year: {analysis['latest_year']}")
    print(f"Risk score: {analysis['risk_score']}")
    print(f"Overall risk: {analysis['overall_risk']}")
    print()

    print("Signals")
    print("-------")
    for name, value in analysis["signals"].items():
        readable_name = name.replace("_", " ").title()
        print(f"{readable_name}: {value}")

    print()
    print("Summary")
    print("-------")
    print(analysis["summary"])
