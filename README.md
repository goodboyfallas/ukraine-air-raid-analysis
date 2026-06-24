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

```bash
git clone https://github.com/YOUR_USERNAME/ukraine-air-raid-analysis.git
cd ukraine-air-raid-analysis
pip install -r requirements.txt
```

## Usage

### Run Pipeline

```bash
python -m src.main
```

### Jupyter Notebook

```bash
cd notebooks
jupyter notebook exploration.ipynb
```

## Project Structure

```text
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
│   ├── visualization/
│   │   └── plotting.py        # Charts
│   └── main.py                # Entry point
├── data/
│   ├── raw/                   # Raw data
│   └── processed/             # Cleaned data
├── notebooks/
│   └── exploration.ipynb      # Jupyter notebook
├── outputs/                   # Generated charts
├── requirements.txt
└── README.md
```

## Data Sources

### Primary (MVP)
- [Vadimkin/ukrainian-air-raid-sirens-dataset](https://github.com/Vadimkin/ukrainian-air-raid-sirens-dataset)

### Optional
- [alerts.in.ua API](https://alerts.in.ua/) - requires token
- [ukrainealarm.com API](https://api.ukrainealarm.com/) - requires access request

## Results

Charts saved to outputs/:
- alerts_over_time.png - alert trend by day
- top_regions.png - top 10 regions
- weekday_heatmap.png - heatmap by day of week and hour
- duration_distribution.png - duration distribution
- weekly_trend.png - weekly trend

## Key Findings

- Dataset: 65,134 oblast-level alerts (Mar 2022 - Jun 2026)
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