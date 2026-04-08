from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate high-level KPIs across dataset quality and distribution."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    kpis: dict[str, object] = {
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "overall_missing_pct": float((df.isna().sum().sum() / (df.shape[0] * max(df.shape[1], 1))) * 100)
        if df.shape[0] > 0
        else 0.0,
        "unique_ratio_by_column": {
            col: float(df[col].nunique(dropna=True) / max(len(df), 1)) for col in df.columns
        },
        "numeric_kpis": {},
    }

    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        kpis["numeric_kpis"][col] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std(ddof=1)) if len(series) > 1 else 0.0,
            "cv": float(series.std(ddof=1) / series.mean()) if len(series) > 1 and series.mean() != 0 else np.nan,
            "p95": float(series.quantile(0.95)),
            "min": float(series.min()),
            "max": float(series.max()),
        }

    return kpis
