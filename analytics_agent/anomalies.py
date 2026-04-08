from __future__ import annotations

import numpy as np
import pandas as pd


def _robust_z_scores(series: pd.Series) -> pd.Series:
    """Compute robust z-scores using median absolute deviation (MAD)."""
    clean = series.astype(float)
    median = clean.median()
    mad = np.median(np.abs(clean - median))
    if mad == 0:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return 0.6745 * (clean - median) / mad


def detect_anomalies(df: pd.DataFrame, threshold: float = 3.5) -> tuple[pd.DataFrame, pd.Series]:
    """Return anomalous rows and row-level anomaly score."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        scores = pd.Series(np.zeros(len(df)), index=df.index, name="anomaly_score")
        return df.iloc[0:0].copy(), scores

    zscore_df = pd.DataFrame(index=df.index)
    for col in numeric_cols:
        col_series = df[col]
        z = _robust_z_scores(col_series.fillna(col_series.median()))
        zscore_df[col] = z.abs()

    anomaly_score = zscore_df.max(axis=1).rename("anomaly_score")
    anomalous_mask = anomaly_score >= threshold

    anomalies = df.loc[anomalous_mask].copy()
    anomalies["anomaly_score"] = anomaly_score[anomalous_mask]
    anomalies = anomalies.sort_values("anomaly_score", ascending=False)

    return anomalies, anomaly_score
