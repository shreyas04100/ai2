"""
Utility functions for dataset inspection, metrics calculation, and before-vs-after comparison table formatting.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

def inspect_dataset_summary(df: pd.DataFrame, name: str = "Dataset") -> Dict[str, Any]:
    """
    Generates comprehensive diagnostic metrics for a dataset.
    """
    summary = {
        "name": name,
        "num_rows": df.shape[0],
        "num_cols": df.shape[1],
        "total_duplicates": df.duplicated().sum(),
        "total_missing_cells": df.isna().sum().sum(),
        "missing_per_column": df.isna().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2)
    }
    return summary

def compute_iqr_outliers(series: pd.Series) -> Tuple[float, float, pd.Series]:
    """
    Computes lower boundary, upper boundary, and outlier mask using the Interquartile Range (IQR) method.
    """
    s_clean = series.dropna()
    q25, q75 = s_clean.quantile(0.25), s_clean.quantile(0.75)
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    outlier_mask = (series < lower_bound) | (series > upper_bound)
    return lower_bound, upper_bound, outlier_mask

def generate_before_after_comparison(raw_df: pd.DataFrame, processed_df: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs a comparative summary table between raw and processed datasets.
    """
    raw_missing = int(raw_df.isna().sum().sum())
    if "TotalCharges" in raw_df.columns:
        raw_missing += int((raw_df["TotalCharges"].astype(str).str.strip() == "").sum())

    comparison_data = {
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Duplicate Rows",
            "Missing Values (Total Cells)",
            "Categorical Columns",
            "Numerical Columns",
            "Memory Usage (KB)"
        ],
        "Raw Dataset": [
            raw_df.shape[0],
            raw_df.shape[1],
            int(raw_df.duplicated().sum()),
            raw_missing,
            len(raw_df.select_dtypes(include=["object", "category"]).columns),
            len(raw_df.select_dtypes(include=["number"]).columns),
            round(raw_df.memory_usage(deep=True).sum() / 1024, 2)
        ],
        "Processed Dataset": [
            processed_df.shape[0],
            processed_df.shape[1],
            int(processed_df.duplicated().sum()),
            int(processed_df.isna().sum().sum()),
            len(processed_df.select_dtypes(include=["object", "category"]).columns),
            len(processed_df.select_dtypes(include=["number"]).columns),
            round(processed_df.memory_usage(deep=True).sum() / 1024, 2)
        ]
    }
    return pd.DataFrame(comparison_data)
