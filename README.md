# Ukraine Air Raid Alerts - Time Series Analysis

Python project for time series analysis of air raid alerts in Ukraine.

## Overview

Analysis of air raid alert patterns: trends, seasonality, regional differences, duration distribution.

### Features

- Data loading from GitHub dataset or alerts.in.ua API
- Data cleaning and normalization
- Feature engineering (day of week, hour, duration)
- Aggregations by region, week, day
- Visualizations: time series, heatmaps, distributions

## Installation

`ash
git clone https://github.com/goodboyfallas/ukraine-air-raid-analysis.git
cd ukraine-air-raid-analysis
pip install -r requirements.txt
`

## Usage

### Run Analysis Pipeline

`ash
python main.py
`

### Explore Data Interactively

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
│   │   └── analytics.py       # Aggregations and statistics
│   └── visualization/
│       └── plotting.py        # Charts
├── data/
│   ├── raw/                   # Raw data
│   └── processed/             # Cleaned data
├── outputs/                   # Generated charts
├── main.py                    # Main pipeline
├── explore.py                 # Data exploration script
├── requirements.txt
└── README.md
`

## Data Sources

### Primary (MVP)
- [Vadimkin/ukrainian-air-raid-sirens-dataset](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset)

### Optional
- [alerts.in.ua API](https://alerts.in.ua/) - requires token
- [ukrainealarm.com API](https://api.ukrainealarm.com/) - requires access request

## Data Notes

- **Geographic level**: Analysis uses oblast-level alerts only (not raion/hromada)
- **2025 data**: Incomplete for Nov-Dec (dataset not fully updated)
- **Duration**: Capped at 24 hours; 0-duration alerts removed
- **Period**: March 2022 - June 2026

## Results

Charts saved to outputs/:
- alerts_over_time.png - alert trend by day
- top_regions.png - top 10 regions
- weekday_heatmap.png - heatmap by day of week and hour
- duration_distribution.png - duration distribution
- weekly_trend.png - weekly trend

## Key Findings

- Dataset: ~65,000 oblast-level alerts (Mar 2022 - Jun 2026)
- Most affected: Donetsk (6,877), Zaporizhzhia (6,686), Kharkiv (6,504)
- Average alert duration: ~80 minutes
- Alerts fairly evenly distributed across weekdays

## Technologies

- Python 3.10+
- pandas, numpy - data processing
- matplotlib, seaborn - visualization
- statsmodels - time series analysis

## Possible Extensions

- Forecasting with Prophet or ARIMA
- Streamlit dashboard
- Live API integration
- Analysis by alert type (missile, aviation, artillery)

## License

MIT