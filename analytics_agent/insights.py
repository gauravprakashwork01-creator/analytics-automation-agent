from __future__ import annotations

from typing import Any


def generate_insights_and_recommendations(
    eda: Any,
    kpis: dict,
    anomaly_count: int,
) -> tuple[list[str], list[str]]:
    """Create lightweight narrative insights and practical recommendations."""
    insights: list[str] = []
    recommendations: list[str] = []

    insights.append(f"Dataset includes {eda.row_count} rows and {eda.column_count} columns.")
    insights.append(
        f"Detected {len(eda.numeric_columns)} numeric and {len(eda.categorical_columns)} categorical columns."
    )

    high_missing = [k for k, v in eda.missing_percentage_by_column.items() if v > 20]
    if high_missing:
        insights.append(f"{len(high_missing)} columns have >20% missing values: {', '.join(high_missing)}.")
        recommendations.append("Impute or drop high-missing columns based on downstream model requirements.")
    else:
        insights.append("No columns exceed 20% missingness.")

    insights.append(f"Anomaly detector flagged {anomaly_count} potential anomalous rows.")
    if anomaly_count > 0:
        recommendations.append("Investigate top anomaly rows for data quality issues or rare business events.")

    overall_missing = kpis.get("overall_missing_pct", 0.0)
    if overall_missing > 5:
        recommendations.append("Add data validation checks at ingestion to reduce missing values.")

    numeric_kpis = kpis.get("numeric_kpis", {})
    for col, metrics in list(numeric_kpis.items())[:3]:
        insights.append(
            f"{col}: mean={metrics['mean']:.2f}, median={metrics['median']:.2f}, p95={metrics['p95']:.2f}."
        )

    if not recommendations:
        recommendations.append("Current data quality appears stable; maintain monitoring with periodic drift checks.")

    return insights, recommendations
