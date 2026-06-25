import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.data.config import OUTPUTS_DIR


def ensure_output_dir() -> Path:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUTS_DIR


def plot_alerts_over_time(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 5))

    if "started_at" in df.columns:
        daily = df.set_index("started_at").resample("D").size()
        ax.plot(daily.index, daily.values, linewidth=0.8, color="#e74c3c")
        ax.fill_between(daily.index, daily.values, alpha=0.2, color="#e74c3c")

    ax.set_title("Air Raid Alerts Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Alerts")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save:
        fig.savefig(ensure_output_dir() / "alerts_over_time.png", dpi=150, bbox_inches="tight")
    return fig


def plot_top_regions(df: pd.DataFrame, n: int = 10, save: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 6))

    from src.analysis.analytics import alerts_by_region
    data = alerts_by_region(df).head(n)

    colors = sns.color_palette("Reds_r", n)
    ax.barh(data["region"], data["alert_count"], color=colors)
    ax.set_title(f"Top {n} Regions by Alert Count", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Alerts")
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()

    if save:
        fig.savefig(ensure_output_dir() / "top_regions.png", dpi=150, bbox_inches="tight")
    return fig


def plot_weekday_heatmap(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    if "weekday" not in df.columns or "hour" not in df.columns:
        print("Warning: weekday/hour columns not found")
        return None

    fig, ax = plt.subplots(figsize=(12, 5))

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = df.pivot_table(index="weekday", columns="hour", values="region", aggfunc="count")
    pivot = pivot.reindex(order)

    sns.heatmap(pivot, cmap="YlOrRd", annot=False, fmt=".0f", ax=ax, cbar_kws={"label": "Alert Count"})
    ax.set_title("Alerts by Day of Week and Hour", fontsize=14, fontweight="bold")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("")
    plt.tight_layout()

    if save:
        fig.savefig(ensure_output_dir() / "weekday_heatmap.png", dpi=150, bbox_inches="tight")
    return fig


def plot_duration_distribution(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    if "duration_minutes" not in df.columns:
        print("Warning: duration_minutes column not found")
        return None

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    df["duration_minutes"].clip(upper=300).hist(bins=50, ax=axes[0], color="#3498db", edgecolor="white")
    axes[0].set_title("Distribution of Alert Duration", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Duration (minutes)")
    axes[0].set_ylabel("Frequency")
    axes[0].axvline(df["duration_minutes"].median(), color="red", linestyle="--", label=f"Median: {df['duration_minutes'].median():.0f} min")
    axes[0].legend()

    if "region" in df.columns:
        from src.analysis.analytics import avg_duration_by_region
        top = avg_duration_by_region(df).head(10)
        axes[1].barh(top["region"], top["avg_duration"], color=sns.color_palette("Blues_r", 10))
        axes[1].set_title("Average Duration by Region (Top 10)", fontsize=12, fontweight="bold")
        axes[1].set_xlabel("Average Duration (minutes)")
        axes[1].invert_yaxis()

    plt.tight_layout()

    if save:
        fig.savefig(ensure_output_dir() / "duration_distribution.png", dpi=150, bbox_inches="tight")
    return fig


def plot_weekly_trend(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    if "started_at" not in df.columns:
        return None

    fig, ax = plt.subplots(figsize=(14, 5))

    weekly = df.set_index("started_at").resample("W").size()
    ax.bar(weekly.index, weekly.values, width=5, color="#e74c3c", alpha=0.7)

    if len(weekly) > 4:
        rolling = weekly.rolling(4).mean()
        ax.plot(rolling.index, rolling.values, color="#2c3e50", linewidth=2, label="4-week moving avg")
        ax.legend()

    ax.set_title("Weekly Alert Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Alerts")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save:
        fig.savefig(ensure_output_dir() / "weekly_trend.png", dpi=150, bbox_inches="tight")
    return fig


def plot_top15_duration(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    if "duration_minutes" not in df.columns or "region" not in df.columns:
        return None

    from src.analysis.analytics import avg_duration_by_region

    fig, ax = plt.subplots(figsize=(12, 8))

    top15 = avg_duration_by_region(df).head(15)

    colors = sns.color_palette("YlOrRd_r", 15)
    bars = ax.barh(top15["region"], top15["avg_duration"], color=colors)

    for bar, val in zip(bars, top15["avg_duration"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f} min", va="center", fontsize=10)

    ax.set_title("Average Alert Duration - Top 15 Regions", fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Duration (minutes)")
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()

    if save:
        fig.savefig(ensure_output_dir() / "top15_duration.png", dpi=150, bbox_inches="tight")
        top15.to_csv(
            ensure_output_dir() / "average_alert_duration_by_region_top15.csv",
            index=False,
            float_format="%.1f",
        )
    return fig


def generate_all_plots(df: pd.DataFrame) -> None:
    print("Generating visualizations...")
    plot_alerts_over_time(df)
    plot_top_regions(df)
    plot_weekday_heatmap(df)
    plot_duration_distribution(df)
    plot_weekly_trend(df)
    print(f"All plots saved to {OUTPUTS_DIR}")
