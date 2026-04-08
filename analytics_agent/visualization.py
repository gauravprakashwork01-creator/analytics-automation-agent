from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def create_charts(df: pd.DataFrame, anomaly_score: pd.Series, charts_dir: Path) -> list[Path]:
    """Generate chart artifacts and return created file paths."""
    created: list[Path] = []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    for col in numeric_cols[:4]:
        fig, ax = plt.subplots(figsize=(7, 4))
        df[col].dropna().plot(kind="hist", bins=30, ax=ax, title=f"Distribution: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        out = charts_dir / f"hist_{col}.png"
        fig.tight_layout()
        fig.savefig(out, dpi=130)
        plt.close(fig)
        created.append(out)

    fig, ax = plt.subplots(figsize=(7, 4))
    anomaly_score.plot(kind="hist", bins=30, ax=ax, title="Anomaly Score Distribution")
    ax.set_xlabel("Anomaly Score")
    ax.set_ylabel("Frequency")
    out = charts_dir / "anomaly_score_distribution.png"
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    created.append(out)

    return created
