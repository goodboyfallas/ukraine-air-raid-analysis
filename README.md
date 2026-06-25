# Ukraine Air Raid Alerts - Time Series Analysis

Python project for time series analysis and forecasting of air raid alerts in Ukraine.

## Overview

Complete analytical system for air raid alert data:
- Data cleaning and preprocessing
- Time series decomposition (trend, seasonality, residuals)
- ACF/PACF statistical analysis
- SARIMA forecasting (30-day horizon with 95% CI)
- K-Means clustering of regions
- Correlation analysis between regions
- Comprehensive visualizations (12 charts)

## Installation

`ash
git clone https://github.com/goodboyfallas/ukraine-air-raid-analysis.git
cd ukraine-air-raid-analysis
pip install -r requirements.txt
`

## Usage

`ash
python main.py
`

## Project Structure

`	ext
ukraine-air-raid-analysis/
├── src/
│   ├── data/
│   │   ├── config.py          # Configuration
│   │   └── loader.py          # Data loading
│   ├── preprocessing/
│   │   └── cleaning.py        # Data cleaning
│   ├── analysis/
│   │   ├── features.py        # Feature engineering
│   │   ├── analytics.py       # Basic aggregations
│   │   ├── decomposition.py   # Time series decomposition
│   │   ├── forecasting.py     # SARIMA forecasting
│   │   └── clustering.py      # K-Means clustering
│   └── visualization/
│       └── plotting.py        # Charts
├── data/
│   ├── raw/                   # Raw data
│   └── processed/             # Cleaned data
├── outputs/                   # Generated charts
├── main.py                    # Entry point
├── requirements.txt
└── README.md
`

## Analysis Pipeline

1. **Data Loading** - GitHub dataset (273k records)
2. **Cleaning** - Filter oblast-level, remove duplicates, cap duration
3. **Features** - Day of week, hour, month, time_of_day
4. **Decomposition** - Trend, seasonality (period=7), residuals
5. **ACF/PACF** - Autocorrelation analysis, ARIMA parameter suggestion
6. **SARIMA** - Auto-tuned (p,d,q)x(P,D,Q,7), 30-day forecast, 95% CI
7. **Clustering** - K-Means on alerts/frequency/duration, elbow method
8. **Correlation** - Cross-region correlation matrix

## Generated Outputs

| Chart | Description |
|-------|-------------|
| alerts_over_time.png | Daily alert trend |
| top_regions.png | Top 10 regions by count |
| weekday_heatmap.png | Day x Hour heatmap |
| duration_distribution.png | Duration histogram |
| weekly_trend.png | Weekly trend with moving avg |
| top15_duration.png | Top 15 regions by duration |
| average_alert_duration_by_region_top15.png | Recalculated Top 15 duration table |
| decomposition.png | Trend/Seasonal/Residual |
| acf_pacf.png | Autocorrelation analysis |
| sarima_forecast.png | 30-day forecast with CI |
| clusters.png | Region clusters scatter |
| elbow.png | Optimal cluster count |
| correlation_matrix.png | Cross-region correlations |

## Key Findings

- **Dataset**: ~65,000 oblast-level alerts (Mar 2022 - Jun 2026)
- **Most affected**: Donetsk (6,877), Zaporizhzhia (6,686), Kharkiv (6,504)
- **Average duration**: ~80 minutes
- **Seasonality**: Weekly pattern detected (period=7)
- **Stationarity**: Non-stationary (requires differencing)
- **Best model**: SARIMA(0,1,2)x(1,1,1,7), AIC=13503

## Data Notes

- Geographic level: oblast-level only (not raion/hromada)
- 2025 data: Incomplete for Nov-Dec
- Duration: Capped at 24h; 0-duration alerts removed

## Technologies

- Python 3.10+
- pandas, numpy - data processing
- matplotlib, seaborn - visualization
- statsmodels - time series analysis, SARIMA
- scikit-learn - K-Means clustering

## License

MIT
