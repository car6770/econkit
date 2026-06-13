"""
EconKit Professional Core Engine
================================

EconKit is a Python toolkit for economics data analysis, teaching, reporting,
and lightweight applied macroeconomic diagnostics.

This module is intentionally self-contained. It avoids heavy dependencies such
as statsmodels or scipy so that the project remains easy to install on GitHub
Actions, beginner-friendly for students, and still useful for serious exploratory
analysis.

Main capabilities
-----------------
1. Dataset loading, cleaning, validation, and profiling
2. Summary statistics, correlations, rolling statistics, and transformations
3. Macroeconomic risk classification
4. Monetary policy stance analysis using a transparent policy-rule benchmark
5. Business-cycle diagnosis and inflation-pressure diagnosis
6. Scenario simulation and scenario comparison
7. Lightweight econometrics: OLS, robust standard errors, simple formula parser
8. Simple forecasting: AR(1), moving-average forecast, scenario projections
9. Markdown report generation and chart generation

Educational and professional-use note
-------------------------------------
EconKit provides transparent, auditable, reproducible calculations. It is useful
for teaching, exploratory analysis, project prototypes, policy memo preparation,
and early-stage research workflows. It is not a substitute for a fully specified
professional forecasting model, central-bank model, or peer-reviewed empirical
research design.
"""

from __future__ import annotations

import json
import math
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


__version__ = "1.1.0"


REQUIRED_MACRO_COLUMNS = [
    "year",
    "gdp_growth",
    "inflation_rate",
    "unemployment_rate",
    "interest_rate",
]

DEFAULT_INDICATORS = [
    "gdp_growth",
    "inflation_rate",
    "unemployment_rate",
    "interest_rate",
]


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------


@dataclass
class DataQualityIssue:
    """A single data-quality issue found in an economic dataset."""

    issue_type: str
    column: Optional[str]
    message: str
    severity: str = "warning"


@dataclass
class DatasetProfile:
    """Compact profile of a loaded economic dataset."""

    rows: int
    columns: int
    column_names: List[str]
    numeric_columns: List[str]
    missing_values: Dict[str, int]
    duplicate_rows: int
    year_min: Optional[int]
    year_max: Optional[int]
    issues: List[DataQualityIssue]


@dataclass
class OLSResult:
    """Container for ordinary least squares regression results."""

    dependent_variable: str
    independent_variables: List[str]
    coefficients: Dict[str, float]
    standard_errors: Dict[str, float]
    t_statistics: Dict[str, float]
    residuals: List[float]
    fitted_values: List[float]
    r_squared: float
    adjusted_r_squared: float
    nobs: int
    df_model: int
    df_resid: int

    def to_dict(self) -> Dict[str, Any]:
        """Return regression results as a plain dictionary."""
        return asdict(self)

    def summary_frame(self) -> pd.DataFrame:
        """Return a coefficient table as a pandas DataFrame."""
        rows = []
        for name in self.coefficients:
            rows.append(
                {
                    "variable": name,
                    "coefficient": self.coefficients[name],
                    "std_error": self.standard_errors.get(name, float("nan")),
                    "t_stat": self.t_statistics.get(name, float("nan")),
                }
            )
        return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# General utilities
# ---------------------------------------------------------------------------


def _is_missing(value: Any) -> bool:
    """Return True if a scalar value should be treated as missing."""
    try:
        return bool(pd.isna(value))
    except Exception:
        return value is None


def _safe_float(value: Any, default: float = float("nan")) -> float:
    """Convert a value to float without crashing."""
    try:
        if _is_missing(value):
            return default
        return float(value)
    except Exception:
        return default


def _safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """Convert a value to int without crashing."""
    try:
        if _is_missing(value):
            return default
        return int(value)
    except Exception:
        return default


def _ensure_path(path: Union[str, Path]) -> Path:
    """Convert a path-like object to pathlib.Path."""
    return Path(path)


def _round_nested(value: Any, digits: int = 2) -> Any:
    """Round floats inside nested structures for readable outputs."""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return value
        return round(value, digits)
    if isinstance(value, dict):
        return {key: _round_nested(val, digits) for key, val in value.items()}
    if isinstance(value, list):
        return [_round_nested(item, digits) for item in value]
    return value


def _validate_required_columns(data: pd.DataFrame, required_columns: Sequence[str]) -> bool:
    """Validate that a DataFrame contains the required columns."""
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return True


def _latest_row(data: pd.DataFrame, year_column: str = "year") -> pd.Series:
    """Return the latest row by year if possible, otherwise by row order."""
    if data.empty:
        raise ValueError("Dataset is empty.")

    if year_column in data.columns:
        return data.sort_values(year_column).iloc[-1]

    return data.iloc[-1]


def _numeric_columns(data: pd.DataFrame) -> List[str]:
    """Return numeric columns in a DataFrame."""
    return list(data.select_dtypes(include=[np.number]).columns)


def _to_markdown_table(data: pd.DataFrame, index: bool = True) -> str:
    """Convert a DataFrame to Markdown with a safe fallback."""
    try:
        return data.to_markdown(index=index)
    except Exception:
        return data.to_string(index=index)


# ---------------------------------------------------------------------------
# Loading, cleaning, validation, and profiling
# ---------------------------------------------------------------------------


def load_economic_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load an economic dataset from CSV, Excel, Parquet, or JSON.

    Parameters
    ----------
    file_path:
        Path to the dataset.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """
    path = _ensure_path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".json":
        return pd.read_json(path)

    raise ValueError(
        f"Unsupported file type: {suffix}. "
        "Supported formats: .csv, .xlsx, .xls, .parquet, .json"
    )


def save_dataset(data: pd.DataFrame, file_path: Union[str, Path], index: bool = False) -> Path:
    """
    Save a dataset to CSV, Excel, Parquet, or JSON based on file extension.
    """
    path = _ensure_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    suffix = path.suffix.lower()

    if suffix == ".csv":
        data.to_csv(path, index=index)
    elif suffix in {".xlsx", ".xls"}:
        data.to_excel(path, index=index)
    elif suffix == ".parquet":
        data.to_parquet(path, index=index)
    elif suffix == ".json":
        data.to_json(path, orient="records", indent=2)
    else:
        raise ValueError(
            f"Unsupported output file type: {suffix}. "
            "Supported formats: .csv, .xlsx, .xls, .parquet, .json"
        )

    return path


def clean_column_names(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy with standardized snake_case column names.
    """
    cleaned = data.copy()
    cleaned.columns = [
        str(column)
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace(".", "_")
        .lower()
        for column in cleaned.columns
    ]
    return cleaned


def coerce_numeric_columns(
    data: pd.DataFrame,
    columns: Optional[Sequence[str]] = None,
    errors: str = "coerce",
) -> pd.DataFrame:
    """
    Return a copy with selected columns converted to numeric values.
    """
    cleaned = data.copy()
    target_columns = list(columns) if columns is not None else list(cleaned.columns)

    for column in target_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors=errors)

    return cleaned


def clean_macro_dataset(
    data: pd.DataFrame,
    required_columns: Sequence[str] = REQUIRED_MACRO_COLUMNS,
    sort_by_year: bool = True,
    drop_duplicate_years: bool = True,
) -> pd.DataFrame:
    """
    Clean a macroeconomic dataset for EconKit analysis.

    This function standardizes column names, converts required columns to numeric
    where appropriate, sorts by year, and optionally drops duplicate years.
    """
    cleaned = clean_column_names(data)

    for column in required_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    if "year" in cleaned.columns:
        cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce")
        cleaned = cleaned.dropna(subset=["year"])
        cleaned["year"] = cleaned["year"].astype(int)

        if drop_duplicate_years:
            cleaned = cleaned.drop_duplicates(subset=["year"], keep="last")

        if sort_by_year:
            cleaned = cleaned.sort_values("year").reset_index(drop=True)

    return cleaned


def validate_macro_dataset(
    data: pd.DataFrame,
    required_columns: Sequence[str] = REQUIRED_MACRO_COLUMNS,
    allow_missing: bool = False,
) -> bool:
    """
    Validate that a macroeconomic dataset is usable by EconKit.
    """
    _validate_required_columns(data, required_columns)

    if data.empty:
        raise ValueError("Dataset is empty.")

    for column in required_columns:
        if column not in data.columns:
            continue

        if not allow_missing and data[column].isna().any():
            missing_count = int(data[column].isna().sum())
            raise ValueError(f"Column '{column}' contains {missing_count} missing values.")

    if "year" in data.columns:
        years = pd.to_numeric(data["year"], errors="coerce")
        if years.isna().any():
            raise ValueError("Column 'year' contains non-numeric values.")
        if years.duplicated().any():
            raise ValueError("Column 'year' contains duplicate years.")

    return True


def profile_dataset(data: pd.DataFrame, required_columns: Sequence[str] = REQUIRED_MACRO_COLUMNS) -> DatasetProfile:
    """
    Build a compact data-quality profile for a dataset.
    """
    issues: List[DataQualityIssue] = []

    for column in required_columns:
        if column not in data.columns:
            issues.append(
                DataQualityIssue(
                    issue_type="missing_required_column",
                    column=column,
                    message=f"Required column '{column}' is missing.",
                    severity="error",
                )
            )

    missing_values = {column: int(data[column].isna().sum()) for column in data.columns}

    for column, count in missing_values.items():
        if count > 0:
            issues.append(
                DataQualityIssue(
                    issue_type="missing_values",
                    column=column,
                    message=f"Column '{column}' contains {count} missing values.",
                    severity="warning",
                )
            )

    duplicate_rows = int(data.duplicated().sum())

    if duplicate_rows > 0:
        issues.append(
            DataQualityIssue(
                issue_type="duplicate_rows",
                column=None,
                message=f"Dataset contains {duplicate_rows} duplicate rows.",
                severity="warning",
            )
        )

    year_min: Optional[int] = None
    year_max: Optional[int] = None

    if "year" in data.columns:
        years = pd.to_numeric(data["year"], errors="coerce")
        if years.notna().any():
            year_min = int(years.min())
            year_max = int(years.max())

        if years.duplicated().any():
            issues.append(
                DataQualityIssue(
                    issue_type="duplicate_years",
                    column="year",
                    message="Dataset contains duplicate years.",
                    severity="warning",
                )
            )

    return DatasetProfile(
        rows=int(len(data)),
        columns=int(len(data.columns)),
        column_names=[str(column) for column in data.columns],
        numeric_columns=_numeric_columns(data),
        missing_values=missing_values,
        duplicate_rows=duplicate_rows,
        year_min=year_min,
        year_max=year_max,
        issues=issues,
    )


def data_quality_report(data: pd.DataFrame, output_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Create a data-quality report. Optionally save it as Markdown.
    """
    profile = profile_dataset(data)

    report = {
        "rows": profile.rows,
        "columns": profile.columns,
        "column_names": profile.column_names,
        "numeric_columns": profile.numeric_columns,
        "missing_values": profile.missing_values,
        "duplicate_rows": profile.duplicate_rows,
        "year_min": profile.year_min,
        "year_max": profile.year_max,
        "issues": [asdict(issue) for issue in profile.issues],
    }

    if output_path is not None:
        path = _ensure_path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "# Data Quality Report",
            "",
            f"- Rows: {profile.rows}",
            f"- Columns: {profile.columns}",
            f"- Year range: {profile.year_min} to {profile.year_max}",
            f"- Duplicate rows: {profile.duplicate_rows}",
            "",
            "## Missing values",
            "",
        ]

        missing_table = pd.DataFrame(
            [{"column": key, "missing_values": value} for key, value in profile.missing_values.items()]
        )
        lines.append(_to_markdown_table(missing_table, index=False))

        lines.extend(["", "## Issues", ""])

        if profile.issues:
            issue_table = pd.DataFrame([asdict(issue) for issue in profile.issues])
            lines.append(_to_markdown_table(issue_table, index=False))
        else:
            lines.append("No issues detected.")

        path.write_text("\n".join(lines), encoding="utf-8")

    return report


# ---------------------------------------------------------------------------
# Basic analysis and visualization
# ---------------------------------------------------------------------------


def calculate_summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate summary statistics for an economic dataset.
    """
    return data.describe()


def calculate_average_growth(data: pd.DataFrame, column: str) -> float:
    """
    Calculate the average value of a selected economic indicator.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")
    return float(data[column].mean())


def find_highest_value_year(data: pd.DataFrame, column: str) -> pd.Series:
    """
    Find the row with the highest value for a selected indicator.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")
    return data.loc[data[column].idxmax()]


def find_lowest_value_year(data: pd.DataFrame, column: str) -> pd.Series:
    """
    Find the row with the lowest value for a selected indicator.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")
    return data.loc[data[column].idxmin()]


def calculate_correlation_matrix(data: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """
    Calculate a correlation matrix for selected economic indicators.
    """
    missing = [column for column in columns if column not in data.columns]
    if missing:
        raise ValueError(f"Columns not found: {missing}")
    return data[list(columns)].corr()


def calculate_rolling_statistics(
    data: pd.DataFrame,
    column: str,
    window: int = 3,
    statistics: Sequence[str] = ("mean", "std"),
) -> pd.DataFrame:
    """
    Calculate rolling statistics for a selected column.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")
    if window <= 0:
        raise ValueError("window must be positive.")

    result = data.copy()
    rolling = result[column].rolling(window=window, min_periods=1)

    if "mean" in statistics:
        result[f"{column}_rolling_mean_{window}"] = rolling.mean()
    if "std" in statistics:
        result[f"{column}_rolling_std_{window}"] = rolling.std()
    if "min" in statistics:
        result[f"{column}_rolling_min_{window}"] = rolling.min()
    if "max" in statistics:
        result[f"{column}_rolling_max_{window}"] = rolling.max()

    return result


def calculate_growth_rates(
    data: pd.DataFrame,
    column: str,
    periods: int = 1,
    multiply_by_100: bool = True,
) -> pd.Series:
    """
    Calculate percent growth rates for a level variable.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")

    rates = data[column].pct_change(periods=periods)
    if multiply_by_100:
        rates = rates * 100
    return rates


def calculate_z_scores(data: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """
    Add z-score columns for selected numeric indicators.
    """
    result = data.copy()

    for column in columns:
        if column not in result.columns:
            raise ValueError(f"Column not found: {column}")

        std = result[column].std(ddof=0)
        if std == 0 or pd.isna(std):
            result[f"{column}_zscore"] = 0.0
        else:
            result[f"{column}_zscore"] = (result[column] - result[column].mean()) / std

    return result


def create_line_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    output_path: Union[str, Path],
    title: Optional[str] = None,
) -> Path:
    """
    Create and save a line chart for an economic indicator.
    """
    if x_column not in data.columns:
        raise ValueError(f"Column not found: {x_column}")
    if y_column not in data.columns:
        raise ValueError(f"Column not found: {y_column}")

    output_path = _ensure_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(data[x_column], data[y_column], marker="o")
    plt.title(title or f"{y_column.replace('_', ' ').title()} Over Time")
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path


def create_multi_line_chart(
    data: pd.DataFrame,
    x_column: str,
    y_columns: Sequence[str],
    output_path: Union[str, Path],
    title: str = "Economic Indicators Over Time",
) -> Path:
    """
    Create and save a multi-line chart for several indicators.
    """
    if x_column not in data.columns:
        raise ValueError(f"Column not found: {x_column}")

    missing = [column for column in y_columns if column not in data.columns]
    if missing:
        raise ValueError(f"Columns not found: {missing}")

    output_path = _ensure_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    for column in y_columns:
        plt.plot(data[x_column], data[column], marker="o", label=column.replace("_", " ").title())

    plt.title(title)
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path


def create_scatter_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    output_path: Union[str, Path],
    title: Optional[str] = None,
) -> Path:
    """
    Create and save a scatter chart for two indicators.
    """
    if x_column not in data.columns:
        raise ValueError(f"Column not found: {x_column}")
    if y_column not in data.columns:
        raise ValueError(f"Column not found: {y_column}")

    output_path = _ensure_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.scatter(data[x_column], data[y_column])
    plt.title(title or f"{y_column.replace('_', ' ').title()} vs {x_column.replace('_', ' ').title()}")
    plt.xlabel(x_column.replace("_", " ").title())
    plt.ylabel(y_column.replace("_", " ").title())
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path


# ---------------------------------------------------------------------------
# Macro classification functions
# ---------------------------------------------------------------------------


def classify_inflation_pressure(inflation_rate: float) -> str:
    """
    Classify inflation pressure based on inflation rate.
    """
    if _is_missing(inflation_rate):
        return "Unknown"

    inflation_rate = float(inflation_rate)

    if inflation_rate >= 4.0:
        return "High"
    if inflation_rate >= 2.5:
        return "Elevated"
    if inflation_rate < 1.0:
        return "Low"
    return "Normal"


def classify_growth_condition(gdp_growth: float) -> str:
    """
    Classify growth condition based on GDP growth.
    """
    if _is_missing(gdp_growth):
        return "Unknown"

    gdp_growth = float(gdp_growth)

    if gdp_growth < 0:
        return "Contraction"
    if gdp_growth < 1.5:
        return "Weak"
    if gdp_growth <= 3.0:
        return "Moderate"
    return "Strong"


def classify_labor_market(unemployment_rate: float) -> str:
    """
    Classify labor market condition based on unemployment rate.
    """
    if _is_missing(unemployment_rate):
        return "Unknown"

    unemployment_rate = float(unemployment_rate)

    if unemployment_rate < 3.0:
        return "Tight"
    if unemployment_rate <= 4.0:
        return "Stable"
    if unemployment_rate <= 5.0:
        return "Soft"
    return "Weak"


def classify_monetary_condition(interest_rate: float) -> str:
    """
    Classify monetary condition based on nominal interest rate.
    """
    if _is_missing(interest_rate):
        return "Unknown"

    interest_rate = float(interest_rate)

    if interest_rate >= 3.0:
        return "Tight"
    if interest_rate >= 1.5:
        return "Neutral"
    return "Accommodative"


def classify_overall_macro_risk(score: int) -> str:
    """
    Classify overall macroeconomic risk from a numeric score.
    """
    if score >= 5:
        return "High"
    if score >= 3:
        return "Elevated"
    if score >= 1:
        return "Moderate"
    return "Low"


def calculate_macro_risk_score(signals: Mapping[str, str]) -> int:
    """
    Calculate a simple macroeconomic risk score from classified signals.
    """
    score = 0

    if signals.get("inflation_pressure") == "High":
        score += 2
    elif signals.get("inflation_pressure") == "Elevated":
        score += 1

    if signals.get("growth_condition") == "Contraction":
        score += 2
    elif signals.get("growth_condition") == "Weak":
        score += 1

    if signals.get("labor_market") == "Weak":
        score += 2
    elif signals.get("labor_market") == "Soft":
        score += 1

    if signals.get("monetary_condition") == "Tight":
        score += 1

    return score


def generate_macro_risk_summary(analysis: Mapping[str, Any]) -> str:
    """
    Generate a readable summary of macroeconomic risk.
    """
    year = analysis["latest_year"]
    signals = analysis["signals"]
    overall_risk = analysis["overall_risk"]

    summary = []
    summary.append(
        f"In {year}, the overall macroeconomic risk level is classified as {overall_risk}."
    )
    summary.append(
        f"Inflation pressure is {signals['inflation_pressure'].lower()}, "
        f"while growth conditions are {signals['growth_condition'].lower()}."
    )
    summary.append(
        f"The labor market is classified as {signals['labor_market'].lower()}, "
        f"and monetary conditions are {signals['monetary_condition'].lower()}."
    )
    summary.append(
        "This classification is based on transparent educational thresholds and "
        "should be interpreted as a screening tool rather than a formal forecast."
    )

    return " ".join(summary)


def analyze_macro_risk(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze macroeconomic risk using the latest observation in the dataset.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    latest = _latest_row(data)

    signals = {
        "inflation_pressure": classify_inflation_pressure(latest["inflation_rate"]),
        "growth_condition": classify_growth_condition(latest["gdp_growth"]),
        "labor_market": classify_labor_market(latest["unemployment_rate"]),
        "monetary_condition": classify_monetary_condition(latest["interest_rate"]),
    }

    risk_score = calculate_macro_risk_score(signals)
    overall_risk = classify_overall_macro_risk(risk_score)

    analysis = {
        "latest_year": int(latest["year"]),
        "latest_values": {
            "gdp_growth": float(latest["gdp_growth"]),
            "inflation_rate": float(latest["inflation_rate"]),
            "unemployment_rate": float(latest["unemployment_rate"]),
            "interest_rate": float(latest["interest_rate"]),
        },
        "signals": signals,
        "risk_score": risk_score,
        "overall_risk": overall_risk,
    }

    analysis["summary"] = generate_macro_risk_summary(analysis)

    return analysis


# ---------------------------------------------------------------------------
# Monetary policy and business-cycle analysis
# ---------------------------------------------------------------------------


def estimate_macro_baseline(data: pd.DataFrame, window: int = 5) -> Dict[str, float]:
    """
    Estimate baseline macroeconomic conditions from recent averages.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    recent = data.sort_values("year").tail(window)

    return {
        "potential_growth": float(recent["gdp_growth"].mean()),
        "target_inflation": 2.0,
        "normal_unemployment": float(recent["unemployment_rate"].mean()),
        "neutral_interest_rate": float(recent["interest_rate"].mean()),
    }


def calculate_real_interest_rate(
    nominal_interest_rate: Union[float, pd.Series],
    inflation_rate: Union[float, pd.Series],
    exact: bool = False,
) -> Union[float, pd.Series]:
    """
    Calculate real interest rate.

    If exact=False, uses Fisher approximation:
        real rate = nominal rate - inflation

    If exact=True, uses:
        real rate = ((1 + nominal/100) / (1 + inflation/100) - 1) * 100
    """
    if exact:
        return ((1 + nominal_interest_rate / 100) / (1 + inflation_rate / 100) - 1) * 100

    return nominal_interest_rate - inflation_rate


def calculate_policy_rule_rate(
    inflation_rate: float,
    gdp_growth: float,
    target_inflation: float = 2.0,
    neutral_interest_rate: float = 2.0,
    potential_growth: float = 2.0,
    inflation_weight: float = 0.5,
    growth_weight: float = 0.5,
) -> float:
    """
    Calculate a transparent policy-rule benchmark interest rate.

    This is inspired by simple monetary policy rules:
        rule = neutral rate
             + inflation_weight * inflation gap
             + growth_weight * growth gap
    """
    inflation_gap = float(inflation_rate) - float(target_inflation)
    growth_gap = float(gdp_growth) - float(potential_growth)

    recommended_rate = (
        float(neutral_interest_rate)
        + float(inflation_weight) * inflation_gap
        + float(growth_weight) * growth_gap
    )

    return float(max(0.0, recommended_rate))


def classify_policy_stance(policy_gap: float) -> str:
    """
    Classify monetary policy stance using actual rate minus benchmark rate.
    """
    policy_gap = float(policy_gap)

    if policy_gap >= 0.75:
        return "Tight"
    if policy_gap >= 0.25:
        return "Moderately Tight"
    if policy_gap <= -0.75:
        return "Accommodative"
    if policy_gap <= -0.25:
        return "Moderately Accommodative"
    return "Neutral"


def generate_monetary_policy_summary(analysis: Mapping[str, Any]) -> str:
    """
    Generate a readable monetary policy stance summary.
    """
    latest_year = analysis["latest_year"]
    stance = analysis["policy_stance"]
    policy_gap = analysis["policy_gap"]
    actual_rate = analysis["actual_interest_rate"]
    recommended_rate = analysis["recommended_policy_rate"]

    if policy_gap > 0:
        direction_text = "above"
    elif policy_gap < 0:
        direction_text = "below"
    else:
        direction_text = "equal to"

    return (
        f"In {latest_year}, monetary policy is classified as {stance}. "
        f"The actual interest rate is {actual_rate:.2f}, while the simple "
        f"policy-rule rate is {recommended_rate:.2f}. "
        f"This means the actual rate is {abs(policy_gap):.2f} percentage points "
        f"{direction_text} the transparent policy-rule benchmark."
    )


def analyze_monetary_policy_stance(
    data: pd.DataFrame,
    target_inflation: float = 2.0,
    neutral_interest_rate: Optional[float] = None,
    potential_growth: Optional[float] = None,
    inflation_weight: float = 0.5,
    growth_weight: float = 0.5,
) -> Dict[str, Any]:
    """
    Analyze whether monetary policy looks tight, neutral, or accommodative.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    baseline = estimate_macro_baseline(data)

    if neutral_interest_rate is None:
        neutral_interest_rate = baseline["neutral_interest_rate"]

    if potential_growth is None:
        potential_growth = baseline["potential_growth"]

    latest = _latest_row(data)

    actual_interest_rate = float(latest["interest_rate"])
    inflation_rate = float(latest["inflation_rate"])
    gdp_growth = float(latest["gdp_growth"])

    recommended_policy_rate = calculate_policy_rule_rate(
        inflation_rate=inflation_rate,
        gdp_growth=gdp_growth,
        target_inflation=target_inflation,
        neutral_interest_rate=neutral_interest_rate,
        potential_growth=potential_growth,
        inflation_weight=inflation_weight,
        growth_weight=growth_weight,
    )

    policy_gap = actual_interest_rate - recommended_policy_rate
    real_interest_rate = calculate_real_interest_rate(actual_interest_rate, inflation_rate)
    policy_stance = classify_policy_stance(policy_gap)

    analysis = {
        "latest_year": int(latest["year"]),
        "actual_interest_rate": round(actual_interest_rate, 2),
        "recommended_policy_rate": round(recommended_policy_rate, 2),
        "policy_gap": round(policy_gap, 2),
        "real_interest_rate": round(float(real_interest_rate), 2),
        "policy_stance": policy_stance,
        "inputs": {
            "inflation_rate": round(inflation_rate, 2),
            "gdp_growth": round(gdp_growth, 2),
            "target_inflation": round(float(target_inflation), 2),
            "neutral_interest_rate": round(float(neutral_interest_rate), 2),
            "potential_growth": round(float(potential_growth), 2),
            "inflation_weight": round(float(inflation_weight), 2),
            "growth_weight": round(float(growth_weight), 2),
        },
        "gaps": {
            "inflation_gap": round(inflation_rate - target_inflation, 2),
            "growth_gap": round(gdp_growth - potential_growth, 2),
        },
    }

    analysis["summary"] = generate_monetary_policy_summary(analysis)

    return analysis


def calculate_output_gap(
    data: pd.DataFrame,
    gdp_growth_column: str = "gdp_growth",
    potential_growth: Optional[float] = None,
    window: int = 5,
) -> pd.Series:
    """
    Calculate a simple output gap proxy using GDP growth minus potential growth.
    """
    if gdp_growth_column not in data.columns:
        raise ValueError(f"Column not found: {gdp_growth_column}")

    if potential_growth is None:
        potential_growth = float(data[gdp_growth_column].tail(window).mean())

    return data[gdp_growth_column] - potential_growth


def classify_business_cycle_phase(
    gdp_growth: float,
    output_gap: float,
    inflation_rate: Optional[float] = None,
) -> str:
    """
    Classify a simple business-cycle phase.
    """
    if gdp_growth < 0:
        return "Recession"
    if gdp_growth < 1.0 and output_gap < 0:
        return "Slowdown"
    if gdp_growth >= 3.0 and output_gap > 0:
        if inflation_rate is not None and inflation_rate >= 3.0:
            return "Overheating"
        return "Expansion"
    if output_gap > 0:
        return "Expansion"
    return "Recovery"


def analyze_business_cycle(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Diagnose the latest business-cycle condition.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    baseline = estimate_macro_baseline(data)
    latest = _latest_row(data)

    output_gap = float(latest["gdp_growth"]) - baseline["potential_growth"]
    phase = classify_business_cycle_phase(
        gdp_growth=float(latest["gdp_growth"]),
        output_gap=output_gap,
        inflation_rate=float(latest["inflation_rate"]),
    )

    analysis = {
        "latest_year": int(latest["year"]),
        "phase": phase,
        "gdp_growth": round(float(latest["gdp_growth"]), 2),
        "estimated_potential_growth": round(baseline["potential_growth"], 2),
        "output_gap_proxy": round(output_gap, 2),
        "inflation_rate": round(float(latest["inflation_rate"]), 2),
        "unemployment_rate": round(float(latest["unemployment_rate"]), 2),
    }

    analysis["summary"] = (
        f"In {analysis['latest_year']}, the economy is classified as {phase}. "
        f"GDP growth is {analysis['gdp_growth']:.2f}, compared with an estimated "
        f"potential growth rate of {analysis['estimated_potential_growth']:.2f}. "
        f"The simple output-gap proxy is {analysis['output_gap_proxy']:.2f}."
    )

    return analysis


def analyze_inflation_pressure(
    data: pd.DataFrame,
    target_inflation: float = 2.0,
    window: int = 3,
) -> Dict[str, Any]:
    """
    Analyze inflation pressure, momentum, and gap relative to target.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    sorted_data = data.sort_values("year")
    latest = sorted_data.iloc[-1]

    inflation = float(latest["inflation_rate"])
    inflation_gap = inflation - target_inflation

    recent = sorted_data["inflation_rate"].tail(window)
    recent_average = float(recent.mean())
    previous = float(sorted_data["inflation_rate"].iloc[-2]) if len(sorted_data) >= 2 else inflation
    momentum = inflation - previous

    pressure = classify_inflation_pressure(inflation)

    if momentum > 0.25:
        momentum_label = "Rising"
    elif momentum < -0.25:
        momentum_label = "Falling"
    else:
        momentum_label = "Stable"

    analysis = {
        "latest_year": int(latest["year"]),
        "inflation_rate": round(inflation, 2),
        "target_inflation": round(target_inflation, 2),
        "inflation_gap": round(inflation_gap, 2),
        "recent_average_inflation": round(recent_average, 2),
        "inflation_momentum": round(momentum, 2),
        "momentum_label": momentum_label,
        "pressure": pressure,
    }

    analysis["summary"] = (
        f"In {analysis['latest_year']}, inflation pressure is classified as {pressure}. "
        f"Inflation is {analysis['inflation_rate']:.2f}, which is "
        f"{abs(analysis['inflation_gap']):.2f} percentage points "
        f"{'above' if analysis['inflation_gap'] >= 0 else 'below'} the target. "
        f"Inflation momentum is {momentum_label.lower()}."
    )

    return analysis


def analyze_policy_mix(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Combine macro risk, policy stance, business cycle, and inflation diagnostics.
    """
    macro_risk = analyze_macro_risk(data)
    policy = analyze_monetary_policy_stance(data)
    cycle = analyze_business_cycle(data)
    inflation = analyze_inflation_pressure(data)

    score = 0

    if macro_risk["overall_risk"] == "High":
        score += 3
    elif macro_risk["overall_risk"] == "Elevated":
        score += 2
    elif macro_risk["overall_risk"] == "Moderate":
        score += 1

    if policy["policy_stance"] in {"Tight", "Accommodative"}:
        score += 1

    if cycle["phase"] in {"Recession", "Overheating"}:
        score += 2
    elif cycle["phase"] == "Slowdown":
        score += 1

    if inflation["pressure"] == "High":
        score += 2
    elif inflation["pressure"] == "Elevated":
        score += 1

    if score >= 6:
        regime = "High tension macro regime"
    elif score >= 4:
        regime = "Elevated tension macro regime"
    elif score >= 2:
        regime = "Mixed macro regime"
    else:
        regime = "Stable macro regime"

    return {
        "regime": regime,
        "score": score,
        "macro_risk": macro_risk,
        "monetary_policy": policy,
        "business_cycle": cycle,
        "inflation_pressure": inflation,
        "summary": (
            f"The current policy mix is classified as a {regime}. "
            f"Macro risk is {macro_risk['overall_risk']}, monetary policy is "
            f"{policy['policy_stance']}, the cycle phase is {cycle['phase']}, "
            f"and inflation pressure is {inflation['pressure']}."
        ),
    }


# ---------------------------------------------------------------------------
# Scenario simulation and forecasting
# ---------------------------------------------------------------------------


def simulate_macro_scenario(
    data: pd.DataFrame,
    scenario_name: str,
    years: int = 5,
    demand_shock: float = 0.0,
    supply_shock: float = 0.0,
    policy_shock: float = 0.0,
) -> pd.DataFrame:
    """
    Simulate a transparent macroeconomic scenario.

    demand_shock:
        Positive values increase growth and inflation.
    supply_shock:
        Positive values increase inflation and reduce growth.
    policy_shock:
        Positive values raise interest rates.
    """
    _validate_required_columns(data, REQUIRED_MACRO_COLUMNS)

    baseline = estimate_macro_baseline(data)
    latest = _latest_row(data)

    previous_gdp_growth = float(latest["gdp_growth"])
    previous_inflation = float(latest["inflation_rate"])
    previous_unemployment = float(latest["unemployment_rate"])

    latest_year = int(latest["year"])

    potential_growth = baseline["potential_growth"]
    target_inflation = baseline["target_inflation"]
    normal_unemployment = baseline["normal_unemployment"]
    neutral_interest_rate = baseline["neutral_interest_rate"]

    results = []

    for step in range(1, int(years) + 1):
        year = latest_year + step
        shock_decay = 0.65 ** (step - 1)

        current_demand_shock = demand_shock * shock_decay
        current_supply_shock = supply_shock * shock_decay
        current_policy_shock = policy_shock * shock_decay

        interest_rate = (
            neutral_interest_rate
            + 0.45 * (previous_inflation - target_inflation)
            + 0.20 * (previous_gdp_growth - potential_growth)
            + current_policy_shock
        )
        interest_rate = max(0.0, interest_rate)

        gdp_growth = (
            0.55 * previous_gdp_growth
            + 0.45 * potential_growth
            + current_demand_shock
            - 0.20 * max(interest_rate - neutral_interest_rate, 0)
            - 0.25 * current_supply_shock
        )

        inflation_rate = (
            0.60 * previous_inflation
            + 0.40 * target_inflation
            + 0.30 * max(gdp_growth - potential_growth, 0)
            + 0.55 * current_supply_shock
            - 0.15 * max(interest_rate - neutral_interest_rate, 0)
        )

        unemployment_rate = (
            0.70 * previous_unemployment
            + 0.30 * normal_unemployment
            - 0.35 * (gdp_growth - potential_growth)
        )
        unemployment_rate = max(0.0, unemployment_rate)

        results.append(
            {
                "scenario": scenario_name,
                "year": year,
                "gdp_growth": round(gdp_growth, 2),
                "inflation_rate": round(inflation_rate, 2),
                "unemployment_rate": round(unemployment_rate, 2),
                "interest_rate": round(interest_rate, 2),
            }
        )

        previous_gdp_growth = gdp_growth
        previous_inflation = inflation_rate
        previous_unemployment = unemployment_rate

    return pd.DataFrame(results)


def build_default_macro_scenarios(data: pd.DataFrame, years: int = 5) -> Dict[str, pd.DataFrame]:
    """
    Build a default scenario set.
    """
    return {
        "baseline": simulate_macro_scenario(data, "baseline", years=years),
        "inflation_shock": simulate_macro_scenario(
            data,
            "inflation_shock",
            years=years,
            supply_shock=2.0,
        ),
        "recession_shock": simulate_macro_scenario(
            data,
            "recession_shock",
            years=years,
            demand_shock=-2.0,
        ),
        "tight_policy": simulate_macro_scenario(
            data,
            "tight_policy",
            years=years,
            policy_shock=1.5,
        ),
    }


def build_stress_test_scenarios(data: pd.DataFrame, years: int = 5) -> Dict[str, pd.DataFrame]:
    """
    Build a richer set of stress-test scenarios.
    """
    return {
        "baseline": simulate_macro_scenario(data, "baseline", years=years),
        "stagflation": simulate_macro_scenario(
            data,
            "stagflation",
            years=years,
            demand_shock=-1.5,
            supply_shock=2.5,
        ),
        "soft_landing": simulate_macro_scenario(
            data,
            "soft_landing",
            years=years,
            demand_shock=0.2,
            supply_shock=-0.5,
            policy_shock=0.2,
        ),
        "hard_landing": simulate_macro_scenario(
            data,
            "hard_landing",
            years=years,
            demand_shock=-2.5,
            policy_shock=1.0,
        ),
        "supply_recovery": simulate_macro_scenario(
            data,
            "supply_recovery",
            years=years,
            supply_shock=-1.5,
        ),
        "policy_mistake": simulate_macro_scenario(
            data,
            "policy_mistake",
            years=years,
            demand_shock=-1.0,
            policy_shock=2.0,
        ),
    }


def compare_macro_scenarios(scenarios: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Compare final-year outcomes across macroeconomic scenarios.
    """
    rows = []

    for scenario_name, scenario_data in scenarios.items():
        final_row = scenario_data.sort_values("year").iloc[-1]
        risk_analysis = analyze_macro_risk(scenario_data)

        rows.append(
            {
                "scenario": scenario_name,
                "final_year": int(final_row["year"]),
                "final_gdp_growth": float(final_row["gdp_growth"]),
                "final_inflation_rate": float(final_row["inflation_rate"]),
                "final_unemployment_rate": float(final_row["unemployment_rate"]),
                "final_interest_rate": float(final_row["interest_rate"]),
                "overall_risk": risk_analysis["overall_risk"],
                "risk_score": risk_analysis["risk_score"],
            }
        )

    return pd.DataFrame(rows)


def forecast_ar1(
    data: pd.DataFrame,
    column: str,
    periods: int = 5,
    year_column: str = "year",
) -> pd.DataFrame:
    """
    Forecast a single indicator with a simple AR(1) model.

    This is a lightweight forecasting tool for transparent baseline projections.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")

    series = pd.to_numeric(data[column], errors="coerce").dropna()

    if len(series) < 3:
        raise ValueError("At least 3 observations are required for AR(1) forecasting.")

    y = series.iloc[1:].to_numpy(dtype=float)
    x = series.iloc[:-1].to_numpy(dtype=float)
    X = np.column_stack([np.ones(len(x)), x])

    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    intercept, phi = float(beta[0]), float(beta[1])

    last_value = float(series.iloc[-1])
    last_year = int(data[year_column].max()) if year_column in data.columns else len(data)

    rows = []
    current = last_value

    for step in range(1, periods + 1):
        current = intercept + phi * current
        rows.append(
            {
                "year": last_year + step,
                "variable": column,
                "forecast": round(float(current), 4),
                "model": "AR(1)",
                "intercept": round(intercept, 4),
                "phi": round(phi, 4),
            }
        )

    return pd.DataFrame(rows)


def forecast_moving_average(
    data: pd.DataFrame,
    column: str,
    periods: int = 5,
    window: int = 3,
    year_column: str = "year",
) -> pd.DataFrame:
    """
    Forecast a single indicator using recent moving average.
    """
    if column not in data.columns:
        raise ValueError(f"Column not found: {column}")

    recent_average = float(pd.to_numeric(data[column], errors="coerce").dropna().tail(window).mean())
    last_year = int(data[year_column].max()) if year_column in data.columns else len(data)

    return pd.DataFrame(
        [
            {
                "year": last_year + step,
                "variable": column,
                "forecast": round(recent_average, 4),
                "model": f"moving_average_{window}",
            }
            for step in range(1, periods + 1)
        ]
    )


def generate_forecast_table(
    data: pd.DataFrame,
    columns: Sequence[str] = DEFAULT_INDICATORS,
    periods: int = 5,
    method: str = "ar1",
) -> pd.DataFrame:
    """
    Generate forecasts for multiple indicators.
    """
    frames = []

    for column in columns:
        if column not in data.columns:
            continue

        if method == "ar1":
            try:
                frames.append(forecast_ar1(data, column, periods=periods))
            except ValueError:
                frames.append(forecast_moving_average(data, column, periods=periods))
        elif method == "moving_average":
            frames.append(forecast_moving_average(data, column, periods=periods))
        else:
            raise ValueError("method must be 'ar1' or 'moving_average'.")

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Lightweight econometrics
# ---------------------------------------------------------------------------


def _prepare_regression_data(
    data: pd.DataFrame,
    y_column: str,
    x_columns: Sequence[str],
    add_constant: bool = True,
) -> Tuple[np.ndarray, np.ndarray, List[str], pd.DataFrame]:
    """
    Prepare arrays for OLS.
    """
    missing = [column for column in [y_column, *x_columns] if column not in data.columns]
    if missing:
        raise ValueError(f"Columns not found: {missing}")

    regression_data = data[[y_column, *x_columns]].copy()
    regression_data = regression_data.apply(pd.to_numeric, errors="coerce").dropna()

    if regression_data.empty:
        raise ValueError("No complete observations are available for regression.")

    y = regression_data[y_column].to_numpy(dtype=float)
    X_raw = regression_data[list(x_columns)].to_numpy(dtype=float)
    variable_names = list(x_columns)

    if add_constant:
        X = np.column_stack([np.ones(len(regression_data)), X_raw])
        variable_names = ["const", *variable_names]
    else:
        X = X_raw

    return y, X, variable_names, regression_data


def _ols_standard_errors(X: np.ndarray, residuals: np.ndarray) -> np.ndarray:
    """
    Calculate conventional OLS standard errors.
    """
    nobs, k = X.shape
    df_resid = max(nobs - k, 1)

    sigma2 = float((residuals.T @ residuals) / df_resid)
    xtx_inv = np.linalg.pinv(X.T @ X)
    covariance = sigma2 * xtx_inv

    return np.sqrt(np.diag(covariance))


def _white_robust_standard_errors(X: np.ndarray, residuals: np.ndarray) -> np.ndarray:
    """
    Calculate White heteroskedasticity-robust standard errors.
    """
    xtx_inv = np.linalg.pinv(X.T @ X)
    meat = X.T @ np.diag(residuals ** 2) @ X
    covariance = xtx_inv @ meat @ xtx_inv

    return np.sqrt(np.diag(covariance))


def run_ols(
    data: pd.DataFrame,
    y_column: str,
    x_columns: Sequence[str],
    add_constant: bool = True,
    robust: bool = False,
) -> OLSResult:
    """
    Run ordinary least squares regression using numpy.

    Parameters
    ----------
    data:
        Input dataset.
    y_column:
        Dependent variable.
    x_columns:
        Independent variables.
    add_constant:
        Whether to include an intercept.
    robust:
        If True, use White heteroskedasticity-robust standard errors.
    """
    y, X, variable_names, regression_data = _prepare_regression_data(
        data,
        y_column=y_column,
        x_columns=x_columns,
        add_constant=add_constant,
    )

    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    fitted = X @ beta
    residuals = y - fitted

    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot != 0 else 0.0

    nobs = int(len(y))
    k = int(X.shape[1])
    df_model = k - 1 if add_constant else k
    df_resid = max(nobs - k, 0)

    if df_resid > 0:
        adjusted_r_squared = 1.0 - (1.0 - r_squared) * (nobs - 1) / df_resid
    else:
        adjusted_r_squared = float("nan")

    if robust:
        standard_errors_array = _white_robust_standard_errors(X, residuals)
    else:
        standard_errors_array = _ols_standard_errors(X, residuals)

    coefficients = {
        name: round(float(value), 6)
        for name, value in zip(variable_names, beta)
    }
    standard_errors = {
        name: round(float(value), 6)
        for name, value in zip(variable_names, standard_errors_array)
    }
    t_statistics = {
        name: round(
            float(coefficients[name] / standard_errors[name])
            if standard_errors[name] != 0
            else float("nan"),
            6,
        )
        for name in coefficients
    }

    return OLSResult(
        dependent_variable=y_column,
        independent_variables=list(x_columns),
        coefficients=coefficients,
        standard_errors=standard_errors,
        t_statistics=t_statistics,
        residuals=[float(value) for value in residuals],
        fitted_values=[float(value) for value in fitted],
        r_squared=round(float(r_squared), 6),
        adjusted_r_squared=round(float(adjusted_r_squared), 6)
        if not math.isnan(adjusted_r_squared)
        else float("nan"),
        nobs=nobs,
        df_model=df_model,
        df_resid=df_resid,
    )


def parse_formula(formula: str) -> Tuple[str, List[str]]:
    """
    Parse a simple formula such as:
        inflation_rate ~ gdp_growth + unemployment_rate
    """
    if "~" not in formula:
        raise ValueError("Formula must contain '~'.")

    left, right = formula.split("~", 1)
    y_column = left.strip()
    x_columns = [part.strip() for part in right.split("+") if part.strip()]

    if not y_column:
        raise ValueError("Formula is missing dependent variable.")
    if not x_columns:
        raise ValueError("Formula is missing independent variables.")

    return y_column, x_columns


def run_ols_formula(
    data: pd.DataFrame,
    formula: str,
    add_constant: bool = True,
    robust: bool = False,
) -> OLSResult:
    """
    Run OLS using a simple formula interface.
    """
    y_column, x_columns = parse_formula(formula)
    return run_ols(
        data,
        y_column=y_column,
        x_columns=x_columns,
        add_constant=add_constant,
        robust=robust,
    )


def regression_report(
    result: OLSResult,
    output_path: Optional[Union[str, Path]] = None,
) -> str:
    """
    Build a Markdown regression report and optionally save it.
    """
    coef_table = result.summary_frame()

    lines = [
        "# Regression Report",
        "",
        f"- Dependent variable: `{result.dependent_variable}`",
        f"- Observations: {result.nobs}",
        f"- R-squared: {result.r_squared:.4f}",
        f"- Adjusted R-squared: {result.adjusted_r_squared:.4f}",
        "",
        "## Coefficients",
        "",
        _to_markdown_table(coef_table, index=False),
        "",
        "## Note",
        "",
        "This regression is estimated with a lightweight EconKit OLS engine. "
        "Use it for transparent exploratory analysis and teaching workflows.",
    ]

    text = "\n".join(lines)

    if output_path is not None:
        path = _ensure_path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    return text


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


def generate_monetary_policy_report(data: pd.DataFrame, output_path: Union[str, Path]) -> Path:
    """
    Generate a Markdown report for monetary policy stance analysis.
    """
    output_path = _ensure_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    analysis = analyze_monetary_policy_stance(data)

    lines = [
        "# Monetary Policy Stance Report",
        "",
        "This report was automatically generated with EconKit.",
        "",
        "## Policy stance",
        "",
        f"- Latest year: {analysis['latest_year']}",
        f"- Policy stance: {analysis['policy_stance']}",
        f"- Actual interest rate: {analysis['actual_interest_rate']:.2f}",
        f"- Recommended policy-rule rate: {analysis['recommended_policy_rate']:.2f}",
        f"- Policy gap: {analysis['policy_gap']:.2f}",
        f"- Real interest rate: {analysis['real_interest_rate']:.2f}",
        "",
        "## Inputs",
        "",
    ]

    for name, value in analysis["inputs"].items():
        lines.append(f"- {name.replace('_', ' ').title()}: {value:.2f}")

    lines.extend(["", "## Economic gaps", ""])

    for name, value in analysis["gaps"].items():
        lines.append(f"- {name.replace('_', ' ').title()}: {value:.2f}")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            analysis["summary"],
            "",
            "## Educational note",
            "",
            "This monetary policy analysis is a simplified transparent tool. "
            "It should not be interpreted as an official policy recommendation.",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def generate_markdown_report(
    data: pd.DataFrame,
    indicators: Sequence[str],
    output_path: Union[str, Path],
) -> Path:
    """
    Generate a Markdown report for economic data.
    """
    output_path = _ensure_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = calculate_summary_statistics(data[list(indicators)])
    correlations = calculate_correlation_matrix(data, indicators)
    macro_risk = analyze_macro_risk(data)
    policy = analyze_monetary_policy_stance(data)
    cycle = analyze_business_cycle(data)
    inflation = analyze_inflation_pressure(data)
    policy_mix = analyze_policy_mix(data)

    lines = [
        "# Economic Data Analysis Report",
        "",
        "This report was automatically generated with EconKit.",
        "",
        "## Dataset overview",
        "",
        f"- Number of observations: {len(data)}",
        f"- Available years: {data['year'].min()} to {data['year'].max()}",
        "",
        "## Executive summary",
        "",
        f"- Overall macro risk: {macro_risk['overall_risk']}",
        f"- Policy stance: {policy['policy_stance']}",
        f"- Business-cycle phase: {cycle['phase']}",
        f"- Inflation pressure: {inflation['pressure']}",
        f"- Policy-mix regime: {policy_mix['regime']}",
        "",
        policy_mix["summary"],
        "",
        "## Summary statistics",
        "",
        _to_markdown_table(summary.round(2)),
        "",
        "## Indicator highlights",
        "",
    ]

    for column in indicators:
        highest = find_highest_value_year(data, column)
        lowest = find_lowest_value_year(data, column)
        average_value = calculate_average_growth(data, column)
        readable_name = column.replace("_", " ").title()

        lines.extend(
            [
                f"### {readable_name}",
                "",
                f"- Average value: {average_value:.2f}",
                f"- Highest value: {highest[column]} in {int(highest['year'])}",
                f"- Lowest value: {lowest[column]} in {int(lowest['year'])}",
                "",
            ]
        )

    lines.extend(
        [
            "## Correlation matrix",
            "",
            _to_markdown_table(correlations.round(2)),
            "",
            "## Macro risk analysis",
            "",
            macro_risk["summary"],
            "",
            "## Monetary policy stance",
            "",
            policy["summary"],
            "",
            "## Business-cycle diagnosis",
            "",
            cycle["summary"],
            "",
            "## Inflation pressure",
            "",
            inflation["summary"],
            "",
            "## Notes",
            "",
            "This report is intended for educational and exploratory use. "
            "It helps users move from raw macroeconomic data to structured interpretation.",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def generate_economic_report(data_path: Union[str, Path], output_dir: Union[str, Path]) -> Path:
    """
    Generate a full economic analysis report from a dataset.
    """
    output_dir = _ensure_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = clean_macro_dataset(load_economic_data(data_path))
    validate_macro_dataset(data)

    indicators = [column for column in DEFAULT_INDICATORS if column in data.columns]

    for indicator in indicators:
        chart_path = output_dir / f"{indicator}.png"
        create_line_chart(data, "year", indicator, chart_path)

    create_multi_line_chart(
        data,
        "year",
        indicators,
        output_dir / "macro_indicators.png",
        title="Macroeconomic Indicators",
    )

    report_path = output_dir / "economic_report.md"
    generate_markdown_report(data, indicators, report_path)

    policy_report_path = output_dir / "monetary_policy_report.md"
    generate_monetary_policy_report(data, policy_report_path)

    quality_report_path = output_dir / "data_quality_report.md"
    data_quality_report(data, quality_report_path)

    return report_path


def generate_macro_scenario_report(
    scenarios: Mapping[str, pd.DataFrame],
    output_path: Union[str, Path],
) -> Path:
    """
    Generate a Markdown report comparing macroeconomic scenarios.
    """
    output_path = _ensure_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    comparison = compare_macro_scenarios(scenarios)

    lines = [
        "# Macro Scenario Analysis Report",
        "",
        "This report was automatically generated with EconKit.",
        "",
        "## Scenario comparison",
        "",
        _to_markdown_table(comparison, index=False),
        "",
        "## Scenario descriptions",
        "",
        "- `baseline`: continuation of recent macroeconomic conditions",
        "- `inflation_shock`: higher inflation caused by a supply-side shock",
        "- `recession_shock`: weaker growth caused by a negative demand shock",
        "- `tight_policy`: higher interest rates caused by a monetary policy shock",
        "- stress-test scenarios may include stagflation, soft landing, hard landing, and policy mistake paths",
        "",
        "## Interpretation guide",
        "",
        "Users can compare scenarios to understand how shocks may affect growth, "
        "inflation, unemployment, interest rates, and overall macro risk.",
        "",
        "## Educational note",
        "",
        "This scenario simulator uses transparent simplified rules. "
        "It is not a professional forecasting model.",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def generate_macro_scenario_analysis(
    data_path: Union[str, Path],
    output_dir: Union[str, Path],
    years: int = 5,
    stress_tests: bool = False,
) -> Dict[str, Any]:
    """
    Generate scenario CSV files, comparison data, and a Markdown report.
    """
    output_dir = _ensure_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = clean_macro_dataset(load_economic_data(data_path))
    validate_macro_dataset(data)

    if stress_tests:
        scenarios = build_stress_test_scenarios(data, years=years)
    else:
        scenarios = build_default_macro_scenarios(data, years=years)

    scenario_paths = {}

    for scenario_name, scenario_data in scenarios.items():
        scenario_path = output_dir / f"{scenario_name}_scenario.csv"
        scenario_data.to_csv(scenario_path, index=False)
        scenario_paths[scenario_name] = scenario_path

    comparison = compare_macro_scenarios(scenarios)
    comparison_path = output_dir / "scenario_comparison.csv"
    comparison.to_csv(comparison_path, index=False)

    report_path = output_dir / "macro_scenario_report.md"
    generate_macro_scenario_report(scenarios, report_path)

    return {
        "scenario_paths": scenario_paths,
        "comparison_path": comparison_path,
        "report_path": report_path,
    }


def generate_full_analysis_package(
    data_path: Union[str, Path],
    output_dir: Union[str, Path],
    years: int = 5,
) -> Dict[str, Any]:
    """
    Generate a full professional-style EconKit analysis package.
    """
    output_dir = _ensure_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = clean_macro_dataset(load_economic_data(data_path))
    validate_macro_dataset(data)

    report_dir = output_dir / "reports"
    chart_dir = output_dir / "charts"
    data_dir = output_dir / "data"
    forecast_dir = output_dir / "forecasts"
    scenario_dir = output_dir / "scenarios"

    report_dir.mkdir(parents=True, exist_ok=True)
    chart_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    forecast_dir.mkdir(parents=True, exist_ok=True)
    scenario_dir.mkdir(parents=True, exist_ok=True)

    cleaned_data_path = data_dir / "cleaned_macro_data.csv"
    data.to_csv(cleaned_data_path, index=False)

    indicators = [column for column in DEFAULT_INDICATORS if column in data.columns]

    chart_paths = []
    for indicator in indicators:
        chart_paths.append(create_line_chart(data, "year", indicator, chart_dir / f"{indicator}.png"))

    chart_paths.append(
        create_multi_line_chart(data, "year", indicators, chart_dir / "macro_indicators.png")
    )

    report_path = generate_markdown_report(data, indicators, report_dir / "economic_report.md")
    policy_report_path = generate_monetary_policy_report(data, report_dir / "monetary_policy_report.md")
    quality_report = data_quality_report(data, report_dir / "data_quality_report.md")

    forecasts = generate_forecast_table(data, indicators, periods=years, method="ar1")
    forecast_path = forecast_dir / "indicator_forecasts.csv"
    forecasts.to_csv(forecast_path, index=False)

    scenario_results = generate_macro_scenario_analysis(
        data_path=cleaned_data_path,
        output_dir=scenario_dir,
        years=years,
        stress_tests=True,
    )

    diagnostics = {
        "macro_risk": analyze_macro_risk(data),
        "monetary_policy": analyze_monetary_policy_stance(data),
        "business_cycle": analyze_business_cycle(data),
        "inflation_pressure": analyze_inflation_pressure(data),
        "policy_mix": analyze_policy_mix(data),
        "data_quality": quality_report,
    }

    diagnostics_path = report_dir / "diagnostics.json"
    diagnostics_path.write_text(
        json.dumps(_round_nested(diagnostics), indent=2),
        encoding="utf-8",
    )

    return {
        "cleaned_data_path": cleaned_data_path,
        "chart_paths": chart_paths,
        "report_path": report_path,
        "policy_report_path": policy_report_path,
        "forecast_path": forecast_path,
        "scenario_results": scenario_results,
        "diagnostics_path": diagnostics_path,
    }


# ---------------------------------------------------------------------------
# Public API helpers
# ---------------------------------------------------------------------------


def quick_analyze(data_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a dataset and return the main EconKit diagnostics in one dictionary.
    """
    data = clean_macro_dataset(load_economic_data(data_path))
    validate_macro_dataset(data)

    return {
        "macro_risk": analyze_macro_risk(data),
        "monetary_policy": analyze_monetary_policy_stance(data),
        "business_cycle": analyze_business_cycle(data),
        "inflation_pressure": analyze_inflation_pressure(data),
        "policy_mix": analyze_policy_mix(data),
    }


def export_json(data: Mapping[str, Any], output_path: Union[str, Path]) -> Path:
    """
    Save a dictionary-like object as pretty JSON.
    """
    path = _ensure_path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_round_nested(dict(data)), indent=2), encoding="utf-8")
    return path


def list_available_features() -> List[str]:
    """
    Return a list of major EconKit capabilities.
    """
    return [
        "dataset loading",
        "dataset cleaning",
        "dataset validation",
        "data quality report",
        "summary statistics",
        "correlation matrix",
        "rolling statistics",
        "z-scores",
        "line charts",
        "multi-line charts",
        "scatter charts",
        "macro risk analysis",
        "monetary policy stance analysis",
        "business-cycle diagnosis",
        "inflation pressure diagnosis",
        "policy-mix analysis",
        "scenario simulation",
        "stress-test scenarios",
        "AR(1) forecasting",
        "moving-average forecasting",
        "OLS regression",
        "formula regression",
        "robust standard errors",
        "Markdown reports",
        "full analysis package",
    ]


__all__ = [
    "__version__",
    "REQUIRED_MACRO_COLUMNS",
    "DEFAULT_INDICATORS",
    "DataQualityIssue",
    "DatasetProfile",
    "OLSResult",
    "load_economic_data",
    "save_dataset",
    "clean_column_names",
    "coerce_numeric_columns",
    "clean_macro_dataset",
    "validate_macro_dataset",
    "profile_dataset",
    "data_quality_report",
    "calculate_summary_statistics",
    "calculate_average_growth",
    "find_highest_value_year",
    "find_lowest_value_year",
    "calculate_correlation_matrix",
    "calculate_rolling_statistics",
    "calculate_growth_rates",
    "calculate_z_scores",
    "create_line_chart",
    "create_multi_line_chart",
    "create_scatter_chart",
    "classify_inflation_pressure",
    "classify_growth_condition",
    "classify_labor_market",
    "classify_monetary_condition",
    "calculate_macro_risk_score",
    "classify_overall_macro_risk",
    "generate_macro_risk_summary",
    "analyze_macro_risk",
    "estimate_macro_baseline",
    "calculate_real_interest_rate",
    "calculate_policy_rule_rate",
    "classify_policy_stance",
    "generate_monetary_policy_summary",
    "analyze_monetary_policy_stance",
    "calculate_output_gap",
    "classify_business_cycle_phase",
    "analyze_business_cycle",
    "analyze_inflation_pressure",
    "analyze_policy_mix",
    "simulate_macro_scenario",
    "build_default_macro_scenarios",
    "build_stress_test_scenarios",
    "compare_macro_scenarios",
    "forecast_ar1",
    "forecast_moving_average",
    "generate_forecast_table",
    "run_ols",
    "parse_formula",
    "run_ols_formula",
    "regression_report",
    "generate_monetary_policy_report",
    "generate_markdown_report",
    "generate_economic_report",
    "generate_macro_scenario_report",
    "generate_macro_scenario_analysis",
    "generate_full_analysis_package",
    "quick_analyze",
    "export_json",
    "list_available_features",
]
