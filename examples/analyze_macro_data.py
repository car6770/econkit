from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    """Load sample economic data."""
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "sample_economic_data.csv"
    return pd.read_csv(data_path)


def show_summary(data):
    """Print basic summary statistics."""
    print("Economic Data Summary")
    print("=====================")
    print(data.describe())


def plot_inflation(data):
    """Plot inflation rate over time."""
    plt.figure()
    plt.plot(data["year"], data["inflation_rate"], marker="o")
    plt.title("Inflation Rate Over Time")
    plt.xlabel("Year")
    plt.ylabel("Inflation Rate (%)")
    plt.grid(True)
    plt.show()


def plot_gdp_growth(data):
    """Plot GDP growth over time."""
    plt.figure()
    plt.plot(data["year"], data["gdp_growth"], marker="o")
    plt.title("GDP Growth Over Time")
    plt.xlabel("Year")
    plt.ylabel("GDP Growth (%)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    data = load_data()
    show_summary(data)
    plot_inflation(data)
    plot_gdp_growth(data)
