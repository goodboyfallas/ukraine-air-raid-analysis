import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import load_csv
from src.preprocessing.cleaning import full_clean
from src.analysis.features import build_features
from src.analysis.analytics import (
    alerts_by_region,
    avg_duration_by_region,
    alerts_by_weekday,
    alerts_by_hour,
    alerts_over_time,
    summary_stats,
)
from src.visualization.plotting import generate_all_plots
from src.data.config import DATA_PROCESSED_DIR


def run_pipeline():
    print("=" * 60)
    print("Ukraine Air Raid Alerts - Time Series Analysis")
    print("=" * 60)

    print("\n[1/5] Loading data...")
    df = load_csv()

    print("\n[2/5] Cleaning data...")
    df = full_clean(df)

    print("\n[3/5] Building features...")
    df = build_features(df)

    print("\n[4/5] Analyzing data...")
    stats = summary_stats(df)
    print(f"\nSummary Statistics:")
    print(f"  Total alerts: {stats['total_alerts']}")
    print(f"  Unique regions: {stats['unique_regions']}")
    if stats["date_range"]:
        print(f"  Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
    if stats["avg_duration"]:
        print(f"  Average duration: {stats['avg_duration']} minutes")

    print(f"\nTop 10 regions:")
    top = alerts_by_region(df).head(10)
    for _, row in top.iterrows():
        print(f"  {row['region']}: {row['alert_count']} alerts")

    print(f"\nAlerts by weekday:")
    weekday_data = alerts_by_weekday(df)
    for _, row in weekday_data.iterrows():
        print(f"  {row['weekday']}: {row['alert_count']}")

    print("\n[5/5] Generating visualizations...")
    generate_all_plots(df)

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_path = DATA_PROCESSED_DIR / "cleaned_alerts.csv"
    df.to_csv(processed_path, index=False)
    print(f"\nProcessed data saved to {processed_path}")

    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)

    return df


if __name__ == "__main__":
    run_pipeline()
