import pandas as pd


def alerts_by_region(df: pd.DataFrame, region_col: str = "region") -> pd.DataFrame:
    result = (
        df.groupby(region_col)
        .size()
        .reset_index(name="alert_count")
        .sort_values("alert_count", ascending=False)
    )
    return result


def avg_duration_by_region(df: pd.DataFrame, region_col: str = "region") -> pd.DataFrame:
    if "duration_minutes" not in df.columns:
        print("Warning: duration_minutes column not found")
        return pd.DataFrame()

    result = (
        df.groupby(region_col)["duration_minutes"]
        .agg(["mean", "median", "max", "count"])
        .round(1)
        .sort_values(["mean", region_col], ascending=[False, True])
        .reset_index()
    )
    result.columns = [region_col, "avg_duration", "median_duration", "max_duration", "count"]
    return result


def alerts_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    if "weekday" not in df.columns:
        return pd.DataFrame()

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    result = df["weekday"].value_counts().reindex(order, fill_value=0).reset_index()
    result.columns = ["weekday", "alert_count"]
    return result


def alerts_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    if "hour" not in df.columns:
        return pd.DataFrame()

    result = df["hour"].value_counts().sort_index().reset_index()
    result.columns = ["hour", "alert_count"]
    return result


def alerts_over_time(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    if "started_at" not in df.columns:
        return pd.DataFrame()

    df_sorted = df.sort_values("started_at")
    result = df_sorted.set_index("started_at").resample(freq).size().reset_index(name="alert_count")
    return result


def top_regions(df: pd.DataFrame, n: int = 10) -> list[str]:
    if "region" not in df.columns:
        return []
    return df["region"].value_counts().head(n).index.tolist()


def summary_stats(df: pd.DataFrame) -> dict:
    stats = {
        "total_alerts": len(df),
        "unique_regions": df["region"].nunique() if "region" in df.columns else 0,
        "date_range": None,
        "avg_duration": None,
    }

    if "started_at" in df.columns:
        stats["date_range"] = {
            "start": str(df["started_at"].min()),
            "end": str(df["started_at"].max()),
        }

    if "duration_minutes" in df.columns:
        stats["avg_duration"] = round(df["duration_minutes"].mean(), 1)

    return stats
