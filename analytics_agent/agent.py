from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .anomalies import detect_anomalies
from .eda import run_basic_eda
from .insights import generate_insights_and_recommendations
from .io_utils import ensure_output_dirs, load_csv
from .kpi import calculate_kpis
from .report import write_report
from .visualization import create_charts


@dataclass
class AgentConfig:
    input_csv: str
    output_dir: str = "outputs"
    anomaly_threshold: float = 3.5


class AnalyticsAutomationAgent:
    """Orchestrates end-to-end analytics automation pipeline."""

    def __init__(self, config: AgentConfig):
        self.config = config

    def run(self) -> Path:
        df = load_csv(self.config.input_csv)
        output_dir, charts_dir = ensure_output_dirs(self.config.output_dir)

        eda_result = run_basic_eda(df)
        kpis = calculate_kpis(df)
        anomalies, anomaly_score = detect_anomalies(df, threshold=self.config.anomaly_threshold)
        insights, recommendations = generate_insights_and_recommendations(eda_result, kpis, len(anomalies))
        chart_paths = create_charts(df, anomaly_score, charts_dir)

        report_path = write_report(
            output_dir=output_dir,
            eda=eda_result,
            kpis=kpis,
            insights=insights,
            recommendations=recommendations,
            anomalies=anomalies,
            chart_paths=chart_paths,
        )
        return report_path
