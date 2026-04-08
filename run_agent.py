from __future__ import annotations

import argparse

from analytics_agent.agent import AgentConfig, AnalyticsAutomationAgent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Analytics Automation Agent")
    parser.add_argument("--input", required=True, help="Path to input CSV dataset")
    parser.add_argument("--output-dir", default="outputs", help="Directory where report artifacts are written")
    parser.add_argument(
        "--anomaly-threshold",
        type=float,
        default=3.5,
        help="Threshold for robust z-score anomaly flagging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = AgentConfig(
        input_csv=args.input,
        output_dir=args.output_dir,
        anomaly_threshold=args.anomaly_threshold,
    )
    agent = AnalyticsAutomationAgent(config)
    report_path = agent.run()
    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
