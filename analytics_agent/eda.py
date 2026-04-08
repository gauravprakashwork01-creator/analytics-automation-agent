from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class EDAResult:
    row_count: int
    column_count: int
    numeric_columns: list[str]
    categorical_columns: list[str]
    missing_percentage_by_column: dict[str, float]
    numeric_summary: dict[str, dict[str, float]]
    categorical_top_values: dict[str, dict[str, int]]


def run_basic_eda(df: pd.DataFrame) -> EDAResult:
    """Run basic EDA and return concise structured results."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols]

    missing_pct = (df.isna().mean() * 100).round(2).to_dict()

    numeric_summary: dict[str, dict[str, float]] = {}
    if numeric_cols:
        summary_df = df[numeric_cols].describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]]
        for col, row in summary_df.iterrows():
            numeric_summary[col] = {k: float(v) for k, v in row.to_dict().items()}

    categorical_top_values: dict[str, dict[str, int]] = {}
    for col in categorical_cols:
        top_vals = df[col].astype("string").fillna("<NA>").value_counts().head(5)
        categorical_top_values[col] = {str(k): int(v) for k, v in top_vals.to_dict().items()}

    return EDAResult(
        row_count=len(df),
        column_count=len(df.columns),
        numeric_columns=numeric_cols,
        categorical_columns=categorical_cols,
        missing_percentage_by_column={k: float(v) for k, v in missing_pct.items()},
        numeric_summary=numeric_summary,
        categorical_top_values=categorical_top_values,
    )
