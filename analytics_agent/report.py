from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def write_report(
    output_dir: Path,
    eda: Any,
    kpis: dict,
    insights: list[str],
    recommendations: list[str],
    anomalies: pd.DataFrame,
    chart_paths: list[Path],
) -> Path:
    """Persist markdown + machine-readable artifacts for downstream consumption."""
    report_path = output_dir / "report.md"

    with report_path.open("w", encoding="utf-8") as f:
        f.write("# Analytics Automation Report\n\n")
        f.write("## Dataset Overview\n")
        f.write(f"- Rows: **{eda.row_count}**\n")
        f.write(f"- Columns: **{eda.column_count}**\n")
        f.write(f"- Numeric columns: **{len(eda.numeric_columns)}**\n")
        f.write(f"- Categorical columns: **{len(eda.categorical_columns)}**\n\n")

        f.write("## KPI Snapshot\n")
        f.write(f"- Overall missing %: **{kpis.get('overall_missing_pct', 0.0):.2f}%**\n")
        f.write(f"- Total rows: **{kpis.get('total_rows', 0)}**\n")
        f.write(f"- Total columns: **{kpis.get('total_columns', 0)}**\n\n")

        f.write("## Insights\n")
        for insight in insights:
            f.write(f"- {insight}\n")
        f.write("\n")

        f.write("## Recommendations\n")
        for rec in recommendations:
            f.write(f"- {rec}\n")
        f.write("\n")

        f.write("## Anomalies\n")
        f.write(f"- Flagged rows: **{len(anomalies)}**\n\n")

        if not anomalies.empty:
            preview = anomalies.head(10).to_markdown(index=False)
            f.write("Top anomaly rows:\n\n")
            f.write(preview + "\n\n")

        f.write("## Charts\n")
        for p in chart_paths:
            rel = p.relative_to(output_dir)
            f.write(f"- ![{p.stem}]({rel.as_posix()})\n")

    (output_dir / "kpis.json").write_text(json.dumps(kpis, indent=2), encoding="utf-8")

    if anomalies.empty:
        anomalies.head(0).to_csv(output_dir / "anomalies.csv", index=False)
    else:
        anomalies.to_csv(output_dir / "anomalies.csv", index=False)

    return report_path
