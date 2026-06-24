import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

from src.data.config import OUTPUTS_DIR


def prepare_daily_series(df: pd.DataFrame, start_date: str = None, end_date: str = None) -> pd.Series:
    if "started_at" not in df.columns:
        raise ValueError("started_at column required")

    filtered = df.copy()
    if start_date:
        filtered = filtered[filtered["started_at"] >= pd.Timestamp(start_date, tz="UTC")]
    if end_date:
        filtered = filtered[filtered["started_at"] <= pd.Timestamp(end_date, tz="UTC")]

    daily = filtered.set_index("started_at").resample("D").size()
    daily = daily.asfreq("D", fill_value=0)
    daily.index.freq = "D"
    return daily


def adf_test(series: pd.Series) -> dict:
    result = adfuller(series.dropna(), autolag="AIC")
    return {
        "test_statistic": round(result[0], 4),
        "p_value": round(result[1], 4),
        "is_stationary": result[1] < 0.05,
    }


def fit_sarima(series: pd.Series, order: tuple = (1, 1, 1), seasonal_order: tuple = (1, 1, 1, 7)):
    print(f"Fitting SARIMA{order}x{seasonal_order}...")

    model = SARIMAX(
        series,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    results = model.fit(disp=False, maxiter=200)

    print(f"AIC: {results.aic:.2f}")
    print(f"BIC: {results.bic:.2f}")

    return results


def forecast_sarima(results, steps: int = 30) -> dict:
    forecast = results.get_forecast(steps=steps)
    mean = forecast.predicted_mean
    conf_int = forecast.conf_int(alpha=0.05)

    return {
        "mean": mean,
        "lower": conf_int.iloc[:, 0],
        "upper": conf_int.iloc[:, 1],
        "steps": steps,
    }


def auto_sarima_params(series: pd.Series) -> tuple:
    adf = adf_test(series)
    d = 0 if adf["is_stationary"] else 1

    best_aic = float("inf")
    best_params = (1, d, 1)
    best_seasonal = (1, d, 1, 7)

    p_range = range(0, 3)
    q_range = range(0, 3)

    for p in p_range:
        for q in q_range:
            try:
                model = SARIMAX(
                    series,
                    order=(p, d, q),
                    seasonal_order=(1, d, 1, 7),
                    enforce_stationarity=False,
                    enforce_invertibility=False,
                )
                result = model.fit(disp=False, maxiter=100)
                if result.aic < best_aic:
                    best_aic = result.aic
                    best_params = (p, d, q)
                    best_seasonal = (1, d, 1, 7)
            except Exception:
                continue

    print(f"Best SARIMA: {best_params}x{best_seasonal} (AIC: {best_aic:.2f})")
    return best_params, best_seasonal


def plot_forecast(series: pd.Series, forecast: dict, save: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 6))

    last_date = series.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast["steps"], freq="D")

    ax.plot(series.index[-90:], series.values[-90:], color="#2c3e50", linewidth=1.2, label="Observed")
    ax.plot(forecast_dates, forecast["mean"].values, color="#e74c3c", linewidth=2, label="Forecast")
    ax.fill_between(
        forecast_dates,
        forecast["lower"].values,
        forecast["upper"].values,
        color="#e74c3c",
        alpha=0.15,
        label="95% CI",
    )

    ax.axvline(x=last_date, color="gray", linestyle="--", alpha=0.5)
    ax.set_title("SARIMA 30-Day Forecast", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Alerts")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save:
        fig.savefig(OUTPUTS_DIR / "sarima_forecast.png", dpi=150, bbox_inches="tight")
    return fig


def forecast_summary(series: pd.Series, forecast: dict) -> dict:
    last_value = series.iloc[-1]
    mean_forecast = forecast["mean"].mean()
    ci_width = (forecast["upper"] - forecast["lower"]).mean()

    return {
        "last_observed": int(last_value),
        "forecast_mean": round(mean_forecast, 1),
        "forecast_lower": round(forecast["lower"].mean(), 1),
        "forecast_upper": round(forecast["upper"].mean(), 1),
        "avg_ci_width": round(ci_width, 1),
        "trend": "increasing" if mean_forecast > last_value else "decreasing",
    }