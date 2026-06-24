import pandas as pd
import requests
from pathlib import Path

from src.data.config import DATA_RAW_DIR, GITHUB_DATASET_URL, ALERTS_IN_UA_TOKEN


def download_github_dataset(save_path: Path | None = None) -> Path:
    if save_path is None:
        save_path = DATA_RAW_DIR / "air_raid_sirens.csv"

    save_path.parent.mkdir(parents=True, exist_ok=True)

    if save_path.exists():
        print(f"Dataset already exists at {save_path}")
        return save_path

    print(f"Downloading dataset from GitHub...")
    response = requests.get(GITHUB_DATASET_URL, timeout=60)
    response.raise_for_status()

    save_path.write_bytes(response.content)
    print(f"Saved to {save_path}")
    return save_path


def load_csv(file_path: Path | None = None) -> pd.DataFrame:
    if file_path is None:
        file_path = DATA_RAW_DIR / "air_raid_sirens.csv"

    if not file_path.exists():
        file_path = download_github_dataset(file_path)

    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records from {file_path}")
    return df


def load_from_alerts_in_ua() -> pd.DataFrame:
    if not ALERTS_IN_UA_TOKEN:
        raise ValueError("ALERTS_IN_UA_TOKEN not set. Use setx ALERTS_IN_UA_TOKEN your_token")

    url = "https://api.alerts.in.ua/v1/alerts/active.json"
    headers = {"Authorization": f"Bearer {ALERTS_IN_UA_TOKEN}"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} active alerts from alerts.in.ua")
    return df
