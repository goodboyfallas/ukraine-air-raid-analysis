
# Development Dialogue Log

Project: Ukraine Air Raid Alerts - Time Series Analysis
Developer: Denis (denispilipcuk638@gmail.com)
Date: 2026-06-24

---

## Initial Request

User asked to act as senior developer-mentor for a test assignment (stage 2):
develop a Python project for time series analysis of air raid alerts in Ukraine.

Goals:
- Create functional project architecture
- Prepare code for GitHub upload (README.md, requirements.txt, .gitignore)
- Write clean, modular code

## Step 1: Planning

Discussed:
- Required libraries: pandas, matplotlib, seaborn, statsmodels, numpy, requests
- Data structure: CSV format with region, started_at, finished_at, duration
- Data sources: GitHub dataset (Vadimkin/ukrainian-air-raid-sirens-dataset), alerts.in.ua API
- Project architecture: src/ with data, preprocessing, analysis, visualization modules

## Step 2: Project Initialization

Created directory structure:
- src/data/ - data loading and config
- src/preprocessing/ - data cleaning
- src/analysis/ - features and analytics
- src/visualization/ - plotting
- data/raw/, data/processed/ - data storage
- notebooks/ - Jupyter exploration
- outputs/ - generated charts

Files created:
- .gitignore - Python template with data/output exclusions
- requirements.txt - pandas, numpy, matplotlib, seaborn, statsmodels, requests, jupyter

## Step 3: Data Loading Module

src/data/config.py:
- PROJECT_ROOT, DATA_RAW_DIR, DATA_PROCESSED_DIR, OUTPUTS_DIR paths
- GITHUB_DATASET_URL for Vadimkin dataset
- ALERTS_IN_UA_TOKEN from environment variable

src/data/loader.py:
- download_github_dataset() - downloads CSV, caches locally
- load_csv() - loads CSV into DataFrame
- load_from_alerts_in_ua() - loads from API (optional)

Issue found: Original URL was 404 (official_data_v2.csv)
Fix: Updated to official_data_en.csv

## Step 4: Preprocessing Module

src/preprocessing/cleaning.py:
- clean_column_names() - normalize to snake_case
- parse_dates() - convert to datetime with UTC
- normalize_regions() - map 25 oblast names to English format
- calculate_duration() - compute duration_minutes
- remove_duplicates() - drop exact duplicates
- rename_columns() - oblast->region, level->location_type
- filter_oblast_level() - filter to oblast-level only (CRITICAL FIX)
- full_clean() - orchestrates all cleaning steps

## Step 5: Analysis Module

src/analysis/features.py:
- add_time_features() - event_date, weekday, hour, month, year, week_number
- add_is_weekend() - boolean flag
- add_time_of_day() - night/morning/afternoon/evening
- build_features() - runs all feature functions

src/analysis/analytics.py:
- alerts_by_region() - count per region
- avg_duration_by_region() - mean/median/max duration
- alerts_by_weekday() - distribution across weekdays
- alerts_by_hour() - distribution across hours
- alerts_over_time() - resampled trend (weekly/monthly)
- top_regions() - top N regions list
- summary_stats() - overall statistics dict

## Step 6: Visualization Module

src/visualization/plotting.py:
- plot_alerts_over_time() - line chart with fill
- plot_top_regions() - horizontal bar chart (top 10)
- plot_weekday_heatmap() - day x hour heatmap
- plot_duration_distribution() - histogram + regional bars
- plot_weekly_trend() - bars with 4-week moving average
- generate_all_plots() - generates all 5 charts

## Step 7: Main Pipeline

src/main.py:
- run_pipeline() - 5-step pipeline:
  1. Load data from GitHub dataset
  2. Clean data (filter oblast-level, remove dupes, parse dates)
  3. Build features (weekday, hour, time_of_day)
  4. Analyze (summary stats, top regions, weekday distribution)
  5. Generate visualizations and save processed CSV

## Step 8: Jupyter Notebook

notebooks/exploration.ipynb:
- 12 cells (markdown + code)
- Loads data, shows stats, generates charts interactively

## Critical Bug Fix: Data Level Mixing

Problem discovered during verification:
- Dataset contains 3 geographic levels: oblast, raion, hromada
- Same alert appears multiple times (once per level)
- Example: Dnipropetrovsk showed 24,018 alerts (all levels) vs 5,565 (oblast only)
- This inflated counts for oblasts with granular raion/hromada data

Solution:
- Added filter_oblast_level() function
- Filters to level == "oblast" before analysis
- Result: 65,134 records (was 159,429)

Corrected statistics:
- Total alerts: 65,134
- Top regions: Donetsk (6,877), Zaporizhzhia (6,686), Kharkiv (6,504)
- Average duration: 79.6 minutes (was 135.8)
- Date range: 2022-03-15 to 2026-06-23

## Step 9: Git Initialization

- git init
- git add . (19 files staged)
- .gitignore correctly excludes data/raw/*, data/processed/*, outputs/*
- Git identity configured: Denis <denispilipcuk638@gmail.com>

## Generated Outputs

5 charts in outputs/:
- alerts_over_time.png (177 KB)
- top_regions.png (52 KB)
- weekday_heatmap.png (50 KB)
- duration_distribution.png (81 KB)
- weekly_trend.png (79 KB)

Processed data: data/processed/cleaned_alerts.csv (65,134 rows, 17 columns)

## Next Steps

- git commit
- Create GitHub repository
- git push to GitHub
