import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from econkit import generate_economic_report


if __name__ == "__main__":
    data_path = project_root / "data" / "sample_economic_data.csv"
    output_dir = project_root / "outputs"

    report_path = generate_economic_report(data_path, output_dir)

    print("Economic report generated successfully.")
    print(f"Report saved to: {report_path}")
