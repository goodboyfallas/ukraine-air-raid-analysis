import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def parse_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
    return df


def normalize_regions(df: pd.DataFrame, region_col: str = "region") -> pd.DataFrame:
    if region_col not in df.columns:
        return df

    region_map = {
        "kyiv": "Kyiv Oblast",
        "kyivska": "Kyiv Oblast",
        "kyiv oblast": "Kyiv Oblast",
        "kyivska oblast": "Kyiv Oblast",
        "kyiv city": "Kyiv City",
        "kharkiv": "Kharkiv Oblast",
        "kharkivska": "Kharkiv Oblast",
        "kharkiv oblast": "Kharkiv Oblast",
        "kharkivska oblast": "Kharkiv Oblast",
        "odesa": "Odesa Oblast",
        "odeska": "Odesa Oblast",
        "odesa oblast": "Odesa Oblast",
        "odeska oblast": "Odesa Oblast",
        "dnipropetrovsk": "Dnipropetrovsk Oblast",
        "dnipropetrovska": "Dnipropetrovsk Oblast",
        "dnipropetrovsk oblast": "Dnipropetrovsk Oblast",
        "dnipropetrovska oblast": "Dnipropetrovsk Oblast",
        "zaporizhzhia": "Zaporizhzhia Oblast",
        "zaporizka": "Zaporizhzhia Oblast",
        "zaporizhzhia oblast": "Zaporizhzhia Oblast",
        "zaporizka oblast": "Zaporizhzhia Oblast",
        "lviv": "Lviv Oblast",
        "lvivska": "Lviv Oblast",
        "lviv oblast": "Lviv Oblast",
        "lvivska oblast": "Lviv Oblast",
        "mykolaiv": "Mykolaiv Oblast",
        "mykolaivska": "Mykolaiv Oblast",
        "mykolaiv oblast": "Mykolaiv Oblast",
        "mykolaivska oblast": "Mykolaiv Oblast",
        "sumy": "Sumy Oblast",
        "sumska": "Sumy Oblast",
        "sumy oblast": "Sumy Oblast",
        "sumska oblast": "Sumy Oblast",
        "chernihiv": "Chernihiv Oblast",
        "chernihivska": "Chernihiv Oblast",
        "chernihiv oblast": "Chernihiv Oblast",
        "chernihivska oblast": "Chernihiv Oblast",
        "poltava": "Poltava Oblast",
        "poltavska": "Poltava Oblast",
        "poltava oblast": "Poltava Oblast",
        "poltavska oblast": "Poltava Oblast",
        "vinnytsia": "Vinnytsia Oblast",
        "vinnytska": "Vinnytsia Oblast",
        "vinnytsia oblast": "Vinnytsia Oblast",
        "vinnytska oblast": "Vinnytsia Oblast",
        "zhytomyr": "Zhytomyr Oblast",
        "zhytomyrska": "Zhytomyr Oblast",
        "zhytomyr oblast": "Zhytomyr Oblast",
        "zhytomyrska oblast": "Zhytomyr Oblast",
        "rivne": "Rivne Oblast",
        "rivnenska": "Rivne Oblast",
        "rivne oblast": "Rivne Oblast",
        "rivnenska oblast": "Rivne Oblast",
        "volyn": "Volyn Oblast",
        "volynska": "Volyn Oblast",
        "volyn oblast": "Volyn Oblast",
        "volynska oblast": "Volyn Oblast",
        "ternopil": "Ternopil Oblast",
        "ternopilska": "Ternopil Oblast",
        "ternopil oblast": "Ternopil Oblast",
        "ternopilska oblast": "Ternopil Oblast",
        "ivano-frankivsk": "Ivano-Frankivsk Oblast",
        "ivano-frankivska": "Ivano-Frankivsk Oblast",
        "ivano-frankivsk oblast": "Ivano-Frankivsk Oblast",
        "ivano-frankivska oblast": "Ivano-Frankivsk Oblast",
        "zakarpattia": "Zakarpattia Oblast",
        "zakarpatska": "Zakarpattia Oblast",
        "zakarpattia oblast": "Zakarpattia Oblast",
        "zakarpatska oblast": "Zakarpattia Oblast",
        "chernivtsi": "Chernivtsi Oblast",
        "chernivetska": "Chernivtsi Oblast",
        "chernivtsi oblast": "Chernivtsi Oblast",
        "chernivetska oblast": "Chernivtsi Oblast",
        "khmelnytskyi": "Khmelnytskyi Oblast",
        "khmelnytska": "Khmelnytskyi Oblast",
        "khmelnytskyi oblast": "Khmelnytskyi Oblast",
        "khmelnytska oblast": "Khmelnytskyi Oblast",
        "cherkasy": "Cherkasy Oblast",
        "cherkaska": "Cherkasy Oblast",
        "cherkasy oblast": "Cherkasy Oblast",
        "cherkaska oblast": "Cherkasy Oblast",
        "kirovohrad": "Kirovohrad Oblast",
        "kirovohradska": "Kirovohrad Oblast",
        "kirovohrad oblast": "Kirovohrad Oblast",
        "kirovohradska oblast": "Kirovohrad Oblast",
        "kherson": "Kherson Oblast",
        "khersonska": "Kherson Oblast",
        "kherson oblast": "Kherson Oblast",
        "khersonska oblast": "Kherson Oblast",
        "donetsk": "Donetsk Oblast",
        "donetska": "Donetsk Oblast",
        "donetsk oblast": "Donetsk Oblast",
        "donetska oblast": "Donetsk Oblast",
        "luhansk": "Luhansk Oblast",
        "luhanska": "Luhansk Oblast",
        "luhansk oblast": "Luhansk Oblast",
        "luhanska oblast": "Luhansk Oblast",
    }

    df[region_col] = (
        df[region_col]
        .str.strip()
        .str.lower()
        .map(region_map)
        .fillna(df[region_col])
    )
    return df


def calculate_duration(df: pd.DataFrame, start_col: str, end_col: str) -> pd.DataFrame:
    if start_col in df.columns and end_col in df.columns:
        df["duration_minutes"] = (
            (df[end_col] - df[start_col]).dt.total_seconds() / 60
        ).round(1)
    return df


def clean_duration(df: pd.DataFrame, max_hours: int = 24) -> pd.DataFrame:
    if "duration_minutes" not in df.columns:
        return df

    before = len(df)
    df = df[df["duration_minutes"] > 0]
    removed_zero = before - len(df)

    max_minutes = max_hours * 60
    outliers = df[df["duration_minutes"] > max_minutes]
    df.loc[df["duration_minutes"] > max_minutes, "duration_minutes"] = max_minutes

    if removed_zero > 0:
        print(f"Removed {removed_zero} alerts with 0 duration")
    if len(outliers) > 0:
        print(f"Capped {len(outliers)} alerts longer than {max_hours}h to {max_minutes} min")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before != after:
        print(f"Removed {before - after} duplicate rows")
    return df


def filter_oblast_level(df: pd.DataFrame) -> pd.DataFrame:
    if "location_type" in df.columns:
        before = len(df)
        df = df[df["location_type"] == "oblast"].copy()
        after = len(df)
        print(f"Filtered to oblast-level: {after} rows (removed {before - after} raion/hromada rows)")
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "oblast": "region",
        "level": "location_type",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df


def full_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = rename_columns(df)
    df = filter_oblast_level(df)

    date_cols = [c for c in df.columns if "time" in c or "date" in c or "started" in c or "finished" in c]
    df = parse_dates(df, date_cols)

    if "region" in df.columns:
        df = normalize_regions(df, "region")

    start_candidates = [c for c in df.columns if "start" in c]
    end_candidates = [c for c in df.columns if "end" in c or "finish" in c]

    if start_candidates and end_candidates:
        df = calculate_duration(df, start_candidates[0], end_candidates[0])

    df = clean_duration(df)
    df = remove_duplicates(df)

    print(f"Cleaned dataset: {len(df)} records, {len(df.columns)} columns")
    return df
