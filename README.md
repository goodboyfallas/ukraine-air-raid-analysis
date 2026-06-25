# Ukraine Air Raid Alerts — Time Series Analysis & Forecasting

Analytical system for studying air raid alert patterns in Ukraine based on data from March 2022 to June 2026.

## What the project does

The system loads air raid alert data, cleans it, and performs a full analysis cycle:

- **Time series decomposition** — extracting trend, seasonality (7-day cycle), and residuals
- **Statistical analysis** — ACF/PACF autocorrelation, ADF stationarity test
- **Forecasting** — SARIMA model with auto-tuned parameters, 30-day forecast with 95% confidence interval
- **Clustering** — K-Means grouping of regions by intensity, frequency, and duration
- **Correlation analysis** — cross-region correlation matrix
- **Visualization** — 12 charts with different data slices

## Installation

```bash
git clone https://github.com/goodboyfallas/ukraine-air-raid-analysis.git
cd ukraine-air-raid-analysis
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

After execution, all generated charts will appear in the outputs/ folder.

## Project structure

```text
ukraine-air-raid-analysis/
├── main.py                          # Entry point - full analysis pipeline
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── .gitignore                       # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── config.py                # Paths, URLs, environment variables
│   │   └── loader.py                # Dataset loading from GitHub
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── cleaning.py              # Cleaning, normalization, filtering
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── features.py              # Feature generation (weekday, hour, month)
│   │   ├── analytics.py             # Aggregations and basic statistics
│   │   ├── decomposition.py         # Time series decomposition, ACF/PACF
│   │   ├── forecasting.py           # SARIMA forecasting model
│   │   └── clustering.py            # K-Means clustering and correlation
│   └── visualization/
│       ├── __init__.py
│       └── plotting.py              # All chart generation functions
├── data/
│   ├── raw/                         # Raw CSV data (downloaded automatically)
│   └── processed/                   # Cleaned data after processing
└── outputs/                         # Generated PNG charts (12 files)
```

## Analysis pipeline

| Step | What happens |
|------|--------------|
| 1. Loading | Download CSV from GitHub (273k records) |
| 2. Cleaning | Filter to oblast-level, remove duplicates, cap duration at 24h |
| 3. Features | Day of week, hour, month, time of day |
| 4. Decomposition | Split into trend + seasonality + residuals |
| 5. ACF/PACF | Autocorrelation analysis, ARIMA parameter selection |
| 6. SARIMA | Train on 2022-2024, forecast 30 days ahead |
| 7. Clustering | K-Means by count/frequency/duration |
| 8. Correlation | Correlation matrix across 24 regions |

## Generated charts

| File | Description |
|------|-------------|
| alerts_over_time.png | Daily alert trend |
| 	op_regions.png | Top 10 regions by count |
| weekday_heatmap.png | Heatmap: day of week x hour |
| duration_distribution.png | Alert duration distribution |
| weekly_trend.png | Weekly trend with moving average |
| top15_duration.png | Top 15 regions by average duration |
| decomposition.png | Trend / Seasonality / Residuals |
| cf_pacf.png | Autocorrelation and partial autocorrelation |
| sarima_forecast.png | 30-day forecast with 95% CI |
| clusters.png | Region clusters |
| elbow.png | Elbow method for optimal cluster count |
| correlation_matrix.png | Cross-region correlation matrix |

## Key results

- **Dataset**: ~65,000 oblast-level alerts (March 2022 - June 2026)
- **Average duration**: ~80 minutes
- **Seasonality**: 7-day cycle confirmed
- **Stationarity**: Series is non-stationary (differencing required)
- **Model**: SARIMA(1,0,2)x(1,0,1,7), AIC=9099
- **Forecast**: ~45 alerts/day, 95% CI [1.4, 88.9]

## Data source

- [Vadimkin/ukrainian-air-raid-sirens-dataset](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset)

## Data notes

- Analysis is performed at oblast level only (raion/hromada excluded)
- Luhansk Oblast excluded (1 record - occupied territory)
- Duration capped at 24 hours; zero-duration alerts removed
- SARIMA trained on 2022-2024 (complete years only)

## Technologies

- **Python 3.10+**
- **pandas**, **numpy** - data processing
- **matplotlib**, **seaborn** - visualization
- **statsmodels** - time series analysis, SARIMA
- **scikit-learn** - K-Means clustering

## License

MIT
