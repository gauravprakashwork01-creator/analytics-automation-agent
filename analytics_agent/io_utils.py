from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load CSV into a DataFrame with lightweight normalization."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")
    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Input file must be a CSV.")

    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    return df


def ensure_output_dirs(base_output_dir: str | Path) -> tuple[Path, Path]:
    """Create output and chart directories."""
    output_dir = Path(base_output_dir)
    charts_dir = output_dir / "charts"
    output_dir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)
    return output_dir, charts_dir
