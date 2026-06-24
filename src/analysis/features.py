import pandas as pd


def add_time_features(df: pd.DataFrame, datetime_col: str = "started_at") -> pd.DataFrame:
    if datetime_col not in df.columns:
        print(f"Warning: column '{datetime_col}' not found")
        return df

    dt = df[datetime_col]
    df["event_date"] = dt.dt.date
    df["weekday"] = dt.dt.day_name()
    df["weekday_num"] = dt.dt.weekday
    df["hour"] = dt.dt.hour
    df["month"] = dt.dt.month
    df["year"] = dt.dt.year
    df["week_number"] = dt.dt.isocalendar().week.astype(int)

    return df


def add_is_weekend(df: pd.DataFrame) -> pd.DataFrame:
    if "weekday_num" in df.columns:
        df["is_weekend"] = df["weekday_num"].isin([5, 6])
    return df


def add_time_of_day(df: pd.DataFrame) -> pd.DataFrame:
    if "hour" not in df.columns:
        return df

    bins = [0, 6, 12, 18, 24]
    labels = ["night", "morning", "afternoon", "evening"]
    df["time_of_day"] = pd.cut(df["hour"], bins=bins, labels=labels, include_lowest=True)
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_time_features(df)
    df = add_is_weekend(df)
    df = add_time_of_day(df)
    print(f"Added features: weekday, hour, month, time_of_day, is_weekend")
    return df
