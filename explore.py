import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.data.loader import load_csv
from src.preprocessing.cleaning import full_clean
from src.analysis.features import build_features
from src.analysis.analytics import (
    alerts_by_region,
    avg_duration_by_region,
    alerts_by_weekday,
    alerts_by_hour,
    summary_stats,
)
from src.visualization.plotting import (
    plot_alerts_over_time,
    plot_top_regions,
    plot_weekday_heatmap,
    plot_duration_distribution,
    plot_weekly_trend,
)

sns.set_style("whitegrid")


def explore():
    print("Loading and cleaning data...")
    df = load_csv()
    df = full_clean(df)
    df = build_features(df)

    print("\n=== DATASET OVERVIEW ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")

    print("\n=== SUMMARY STATISTICS ===")
    stats = summary_stats(df)
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n=== TOP 10 REGIONS ===")
    top = alerts_by_region(df).head(10)
    print(top.to_string(index=False))

    print("\n=== ALERTS BY WEEKDAY ===")
    weekday = alerts_by_weekday(df)
    print(weekday.to_string(index=False))

    print("\n=== ALERTS BY HOUR ===")
    hourly = alerts_by_hour(df)
    print(hourly.to_string(index=False))

    print("\n=== DURATION STATS ===")
    if "duration_minutes" in df.columns:
        print(df["duration_minutes"].describe())

    print("\n=== GENERATING PLOTS ===")
    plot_alerts_over_time(df, save=True)
    print("  - alerts_over_time.png")
    plot_top_regions(df, save=True)
    print("  - top_regions.png")
    plot_weekday_heatmap(df, save=True)
    print("  - weekday_heatmap.png")
    plot_duration_distribution(df, save=True)
    print("  - duration_distribution.png")
    plot_weekly_trend(df, save=True)
    print("  - weekly_trend.png")

    print("\nDone! Check outputs/ folder for charts.")

    return df


if __name__ == "__main__":
    explore()