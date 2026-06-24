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
- Comprehensive visualizations

## Installation

`ash
git clone https://github.com/goodboyfallas/ukraine-air-raid-analysis.git
cd ukraine-air-raid-analysis
pip install -r requirements.txt
`

## Usage

### Basic Analysis

`ash
python main.py
`

### Advanced Analysis (Full Pipeline)

`ash
python main_advanced.py
`

### Data Exploration

`ash
python explore.py
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
├── main.py                    # Basic pipeline
├── main_advanced.py           # Advanced analysis pipeline
├── explore.py                 # Data exploration
├── requirements.txt
└── README.md
`

## Analysis Modules

### 1. Data Preparation
- Daily aggregation of alert counts
- 7-day and 30-day moving averages
- Duration outlier removal (0 min, >24h)

### 2. Time Series Decomposition
- Additive decomposition with 7-day period
- Separates trend, seasonality, residuals
- ADF stationarity test

### 3. Statistical Analysis
- ACF (Autocorrelation Function)
- PACF (Partial Autocorrelation Function)
- Automatic ARIMA parameter suggestion

### 4. SARIMA Forecasting
- Auto-tuned parameters (p,d,q)x(P,D,Q,s)
- 30-day forecast horizon
- 95% confidence intervals
- AIC/BIC model evaluation

### 5. Region Clustering
- K-Means algorithm
- Features: total alerts, frequency, duration
- Elbow method for optimal k
- StandardScaler normalization

### 6. Correlation Analysis
- Cross-region correlation matrix
- Identifies synchronized alert patterns

## Generated Outputs

| Chart | Description |
|-------|-------------|
| alerts_over_time.png | Daily alert trend |
| top_regions.png | Top 10 regions by count |
| weekday_heatmap.png | Day x Hour heatmap |
| duration_distribution.png | Duration histogram |
| weekly_trend.png | Weekly trend with moving avg |
| top15_duration.png | Top 15 regions by duration |
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