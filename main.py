import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data.loader import load_csv
from src.preprocessing.cleaning import full_clean
from src.analysis.features import build_features
from src.analysis.analytics import summary_stats
from src.analysis.decomposition import (
    add_moving_averages,
    adf_test,
    decompose_series,
    calc_acf_pacf,
    suggest_arima_params,
    plot_decomposition,
    plot_acf_pacf,
)
from src.analysis.forecasting import (
    prepare_daily_series,
    fit_sarima,
    forecast_sarima,
    auto_sarima_params,
    plot_forecast,
    forecast_summary,
)
from src.analysis.clustering import (
    build_region_features,
    correlation_matrix,
    cluster_regions,
    find_optimal_k,
    plot_correlation_matrix,
    plot_clusters,
    plot_elbow,
)
from src.visualization.plotting import (
    plot_alerts_over_time,
    plot_top_regions,
    plot_weekday_heatmap,
    plot_duration_distribution,
    plot_weekly_trend,
    plot_top15_duration,
)
from src.data.config import DATA_PROCESSED_DIR, OUTPUTS_DIR


def run_advanced_analysis():
    print("=" * 60)
    print("Air Raid Alerts - Advanced Time Series Analysis")
    print("=" * 60)

    print("\n[1/8] Loading and cleaning data...")
    df = load_csv()
    df = full_clean(df)
    df = build_features(df)

    print("\n[2/8] Preparing daily time series...")
    daily = prepare_daily_series(df)
    daily_ma = add_moving_averages(daily)

    print(f"  Daily series: {len(daily)} days")
    print(f"  Mean alerts/day: {daily.mean():.1f}")
    print(f"  Max alerts/day: {daily.max()}")

    print("\n[3/8] Stationarity test (ADF)...")
    adf_result = adf_test(daily)
    print(f"  ADF Statistic: {adf_result['test_statistic']}")
    print(f"  p-value: {adf_result['p_value']}")
    print(f"  Stationary: {adf_result['is_stationary']}")

    print("\n[4/8] Time series decomposition...")
    decomp = decompose_series(daily, model="additive", period=7)
    plot_decomposition(daily, decomp)
    print("  Saved: decomposition.png")

    print("\n[5/8] ACF/PACF analysis...")
    acf_pacf = calc_acf_pacf(daily)
    arima_params = suggest_arima_params(daily)
    plot_acf_pacf(daily)
    print(f"  Suggested ARIMA params: {arima_params}")
    print("  Saved: acf_pacf.png")

    print("\n[6/8] SARIMA forecasting (30 days)...")
    print("  Training on 2022-2024 (complete years only)...")
    daily_train = prepare_daily_series(df, start_date="2022-01-01", end_date="2024-12-31")
    print(f"  Training series: {len(daily_train)} days")
    params, seasonal = auto_sarima_params(daily_train)
    sarima_result = fit_sarima(daily_train, order=params, seasonal_order=seasonal)
    forecast = forecast_sarima(sarima_result, steps=30)
    plot_forecast(daily_train, forecast)
    print("  Saved: sarima_forecast.png")

    summary = forecast_summary(daily_train, forecast)
    print(f"\n  Forecast Summary:")
    print(f"    Training period: 2022-01-01 to 2024-12-31")
    print(f"    Last observed: {summary['last_observed']} alerts")
    print(f"    Forecast mean: {summary['forecast_mean']} alerts/day")
    print(f"    95% CI: [{summary['forecast_lower']}, {summary['forecast_upper']}]")
    print(f"    Trend: {summary['trend']}")

    print("\n[7/8] Region clustering...")
    features = build_region_features(df)
    optimal_k = find_optimal_k(features)
    print(f"  Optimal clusters: {optimal_k}")
    features = cluster_regions(features, n_clusters=optimal_k)
    plot_clusters(features)
    plot_elbow(features)
    print("  Saved: clusters.png, elbow.png")

    print("\n[8/8] Correlation analysis...")
    corr = correlation_matrix(df)
    plot_correlation_matrix(corr)
    print("  Saved: correlation_matrix.png")

    print("\n[Visualizations] Generating standard plots...")
    plot_alerts_over_time(df)
    plot_top_regions(df)
    plot_weekday_heatmap(df)
    plot_duration_distribution(df)
    plot_weekly_trend(df)
    plot_top15_duration(df)
    print("  All standard plots saved")

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_path = DATA_PROCESSED_DIR / "cleaned_alerts.csv"
    df.to_csv(processed_path, index=False)

    print("\n" + "=" * 60)
    print("Advanced analysis completed!")
    print(f"Results saved to: {OUTPUTS_DIR}")
    print("=" * 60)

    return df, daily, forecast, features, corr


if __name__ == "__main__":
    run_advanced_analysis()