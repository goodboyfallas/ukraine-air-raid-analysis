import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf

from src.data.config import OUTPUTS_DIR


def prepare_daily_series(df: pd.DataFrame) -> pd.Series:
    if "started_at" not in df.columns:
        raise ValueError("started_at column required")

    daily = df.set_index("started_at").resample("D").size()
    daily = daily.asfreq("D", fill_value=0)
    daily.index.freq = "D"
    return daily


def add_moving_averages(series: pd.Series) -> pd.DataFrame:
    result = pd.DataFrame({"alerts": series})
    result["ma_7"] = series.rolling(window=7, min_periods=1).mean()
    result["ma_30"] = series.rolling(window=30, min_periods=1).mean()
    return result


def adf_test(series: pd.Series) -> dict:
    result = adfuller(series.dropna(), autolag="AIC")
    return {
        "test_statistic": round(result[0], 4),
        "p_value": round(result[1], 4),
        "lags_used": result[2],
        "n_observations": result[3],
        "critical_values": {k: round(v, 4) for k, v in result[4].items()},
        "is_stationary": result[1] < 0.05,
    }


def decompose_series(series: pd.Series, model: str = "additive", period: int = 7) -> dict:
    decomposition = seasonal_decompose(series, model=model, period=period)

    return {
        "observed": decomposition.observed,
        "trend": decomposition.trend,
        "seasonal": decomposition.seasonal,
        "residual": decomposition.resid,
    }


def calc_acf_pacf(series: pd.Series, nlags: int = 40) -> dict:
    diff_series = series.diff().dropna()
    acf_vals = acf(diff_series, nlags=nlags, fft=True)
    pacf_vals = pacf(diff_series, nlags=nlags)

    return {
        "acf": acf_vals,
        "pacf": pacf_vals,
        "nlags": nlags,
    }


def suggest_arima_params(series: pd.Series) -> tuple[int, int, int]:
    acf_pacf = calc_acf_pacf(series, nlags=20)
    acf_vals = acf_pacf["acf"][1:]
    pacf_vals = acf_pacf["pacf"][1:]

    acf_cutoff = 1.96 / np.sqrt(len(series))
    pacf_cutoff = 1.96 / np.sqrt(len(series))

    q = 0
    for i, val in enumerate(acf_vals):
        if abs(val) > acf_cutoff:
            q = i + 1
        else:
            break

    p = 0
    for i, val in enumerate(pacf_vals):
        if abs(val) > pacf_cutoff:
            p = i + 1
        else:
            break

    p = min(p, 5)
    q = min(q, 5)

    adf_result = adf_test(series)
    d = 0 if adf_result["is_stationary"] else 1

    return (p, d, q)


def plot_decomposition(series: pd.Series, decomp: dict, save: bool = True) -> plt.Figure:
    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

    axes[0].plot(decomp["observed"], color="#2c3e50", linewidth=0.8)
    axes[0].set_title("Observed", fontsize=12, fontweight="bold")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(decomp["trend"], color="#e74c3c", linewidth=1.2)
    axes[1].set_title("Trend", fontsize=12, fontweight="bold")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(decomp["seasonal"], color="#3498db", linewidth=0.8)
    axes[2].set_title("Seasonal (period=7)", fontsize=12, fontweight="bold")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(decomp["residual"], color="#27ae60", linewidth=0.8)
    axes[3].set_title("Residual", fontsize=12, fontweight="bold")
    axes[3].grid(True, alpha=0.3)

    plt.suptitle("Time Series Decomposition", fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()

    if save:
        fig.savefig(OUTPUTS_DIR / "decomposition.png", dpi=150, bbox_inches="tight")
    return fig


def plot_acf_pacf(series: pd.Series, save: bool = True) -> plt.Figure:
    acf_pacf = calc_acf_pacf(series)

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    acf_vals = acf_pacf["acf"]
    pacf_vals = acf_pacf["pacf"]
    nlags = acf_pacf["nlags"]
    conf = 1.96 / np.sqrt(len(series))

    axes[0].bar(range(len(acf_vals)), acf_vals, color="#3498db", width=0.3)
    axes[0].axhline(y=conf, color="red", linestyle="--", alpha=0.5)
    axes[0].axhline(y=-conf, color="red", linestyle="--", alpha=0.5)
    axes[0].set_title("Autocorrelation Function (ACF)", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Lag")

    axes[1].bar(range(len(pacf_vals)), pacf_vals, color="#e74c3c", width=0.3)
    axes[1].axhline(y=conf, color="red", linestyle="--", alpha=0.5)
    axes[1].axhline(y=-conf, color="red", linestyle="--", alpha=0.5)
    axes[1].set_title("Partial Autocorrelation Function (PACF)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Lag")

    plt.tight_layout()

    if save:
        fig.savefig(OUTPUTS_DIR / "acf_pacf.png", dpi=150, bbox_inches="tight")
    return fig