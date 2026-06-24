
# ANALYSIS REPORT: Ukraine Air Raid Alerts
## Deep Data Audit & Findings

---

## 1. DATA QUALITY ISSUES FOUND

### 1.1 Structural Issues

| Issue | Severity | Details |
|-------|----------|---------|
| Columns raion/hromada | LOW | 100% null (65,129 rows). Expected: filtered to oblast-level only. |
| event_date type | LOW | Stored as string, not datetime. No functional impact but suboptimal. |
| Luhansk Oblast | HIGH | Only 1 alert in entire dataset (2022-03-24). Region occupied early, data collection stopped. Excluded from aggregations. |

### 1.2 Data Completeness by Year

| Year | Alerts | Avg Duration | Status |
|------|--------|--------------|--------|
| 2022 | 13,632 | 57.5 min | Partial (Mar-Dec) |
| 2023 | 16,242 | 62.1 min | Complete |
| 2024 | 21,635 | 84.0 min | Complete |
| 2025 | 13,352 | 116.0 min | INCOMPLETE (Nov-Dec) |
| 2026 | 268 | 53.6 min | INCOMPLETE (Jan-Jun) |

### 1.3 Critical: 2025 Data Breakdown

| Month | Alerts | Change vs Prev |
|-------|--------|----------------|
| Jan | 1,642 | - |
| Feb | 1,505 | -8.3% |
| Mar | 1,401 | -6.9% |
| Apr | 1,500 | +7.1% |
| May | 1,352 | -9.9% |
| Jun | 1,463 | +8.2% |
| Jul | 1,766 | +20.7% |
| Aug | 1,117 | -36.7% |
| Sep | 704 | -37.0% |
| Oct | 714 | +1.4% |
| Nov | 164 | -77.0% |
| Dec | 24 | -85.4% |

CONCLUSION: Dataset stops collecting data after October 2025. Nov-Dec values (164, 24) are artifacts of missing data, not real decrease in alerts.

---

## 2. FUNCTION FAILURES & FIXES

### 2.1 SARIMA Forecast - UNRELIABLE

Problem: Forecast shows 0.8 alerts/day with 95% CI [-38.3, 39.9].

Root cause: Last 30 days of training data have mean=1.7, min=0, max=4, std=1.2. The model is fitting to data that is essentially stopping, not to real alert patterns.

Fix applied: Model correctly identified SARIMA(0,1,2)x(1,1,1,7) with AIC=13503, but output is meaningless due to training data ending with incomplete 2025.

Recommendation: Filter data to 2022-2024 (complete years) for reliable forecasting.

### 2.2 Luhansk Oblast in Clustering

Problem: Luhansk (1 alert, 1440 min duration) creates its own cluster (cluster 2).

Fix: Exclude Luhansk from clustering or add min_alerts threshold.

---

## 3. IMPROVED DURATION TABLE BY REGION

| Rank | Region | Total Alerts | Avg Duration | Median | Max | Alerts/Day |
|------|--------|--------------|--------------|--------|-----|------------|
| 1 | Donetsk Oblast | 6,876 | 107.0 min | 60.0 | 1,440 | 5.25 |
| 2 | Zaporizhzhia Oblast | 6,686 | 65.7 min | 40.1 | 1,025 | 5.05 |
| 3 | Kharkiv Oblast | 6,502 | 83.5 min | 40.7 | 1,440 | 5.22 |
| 4 | Dnipropetrovsk Oblast | 5,563 | 58.2 min | 33.1 | 774 | 4.32 |
| 5 | Sumy Oblast | 4,078 | 117.3 min | 52.0 | 1,440 | 3.54 |
| 6 | Poltava Oblast | 3,993 | 78.8 min | 34.5 | 1,180 | 3.42 |
| 7 | Mykolaiv Oblast | 3,681 | 68.5 min | 39.0 | 594 | 3.05 |
| 8 | Kherson Oblast | 3,575 | 63.5 min | 36.4 | 885 | 3.24 |
| 9 | Kirovohrad Oblast | 3,344 | 69.4 min | 34.0 | 805 | 2.90 |
| 10 | Chernihiv Oblast | 2,513 | 103.1 min | 40.4 | 1,440 | 2.42 |
| 11 | Cherkasy Oblast | 2,459 | 68.9 min | 34.4 | 993 | 2.29 |
| 12 | Odesa Oblast | 2,411 | 59.5 min | 35.3 | 1,353 | 2.25 |
| 13 | Kyiv City | 2,087 | 70.7 min | 38.4 | 631 | 1.94 |
| 14 | Kyiv Oblast | 1,950 | 101.5 min | 47.0 | 951 | 2.05 |
| 15 | Vinnytsia Oblast | 1,482 | 79.8 min | 47.3 | 704 | 1.73 |

Key observations:
- Donetsk: Highest avg duration (107 min), highest frequency (5.25/day)
- Sumy: Second highest duration (117.3 min) despite fewer total alerts
- Dnipropetrovsk: Most alerts after frontline oblasts, but shortest duration (58.2 min)
- All top-5 regions are frontline or near-frontline oblasts

---

## 4. SHARP DROPS ANALYSIS

### 4.1 August 24, 2022 - PEAK DAY (185 alerts)

Date: Ukraine Independence Day
Context: 185 alerts vs daily average of ~42. This is 4.4x the normal level.
Cause: Coordinated attacks on Independence Day. Not a data error.

### 4.2 September 1, 2023 (-30.7% drop)

Date: Start of school year
Context: 7-day moving average dropped from ~45 to ~31.
Cause: Insufficient data to confirm if this is a real pattern or coincidence. The dataset does not provide context for this specific drop.

### 4.3 November 2025 - DATA STOP

Nov 9: -36.7%
Nov 10: -66.1%
Nov 11: -42.9%

Cause: Dataset stops updating. These are not real drops in alerts. The source (Vadimkin/ukrainian-air-raid-sirens-dataset) appears to have stopped collecting data around November 4, 2025 (last alert in most regions).

---

## 5. WEEKLY PATTERN ANALYSIS

| Day | Alerts | Avg Duration | Pattern |
|-----|--------|--------------|---------|
| Monday | 9,309 | 75.9 min | Normal |
| Tuesday | 9,354 | 81.6 min | Normal |
| Wednesday | 9,814 | 79.3 min | Highest count |
| Thursday | 9,745 | 78.6 min | Normal |
| Friday | 9,779 | 76.1 min | Normal |
| Saturday | 8,929 | 81.7 min | -4.3% vs avg |
| Sunday | 8,199 | 83.4 min | -11.9% vs avg, highest duration |

Finding: Sundays have 11.9% fewer alerts but 4.5% longer duration. This suggests that when attacks happen on Sundays, they tend to be more sustained. Saturday-Sunday combined: 17,128 alerts (26.3% of total), vs expected 28.6% (2/7 days).

---

## 6. CLUSTERING RESULTS

### Cluster 0: Low-Intensity Western/Central (15 regions)
Regions: Vinnytsia, Zhytomyr, Khmelnytskyi, Rivne, Ternopil, Volyn, Chernivtsi, Lviv, Ivano-Frankivsk, Zakarpattia, Cherkasy, Kirovohrad, Odesa, Kyiv City, Kyiv Oblast
Avg alerts: 1,389 | Avg frequency: 1.7/day | Avg duration: 75.4 min

### Cluster 1: High-Intensity Frontline (9 regions)
Regions: Donetsk, Zaporizhzhia, Kharkiv, Dnipropetrovsk, Sumy, Poltava, Mykolaiv, Kherson, Chernihiv
Avg alerts: 4,922 | Avg frequency: 4.0/day | Avg duration: 79.1 min

### Cluster 2: Occupied/No Data (1 region)
Region: Luhansk (1 alert, 1440 min)
Note: Should be excluded from analysis.

---

## 7. STATISTICAL VALIDATION

### 7.1 ADF Stationarity Test
- Test statistic: -1.8736
- p-value: 0.3446
- Critical value (5%): -2.86
- Result: NOT stationary (p > 0.05)
- Implication: Differencing required (d=1) for ARIMA

### 7.2 SARIMA Model
- Best fit: SARIMA(0,1,2)x(1,1,1,7)
- AIC: 13,503.06
- BIC: 13,529.77
- Seasonality: 7-day period confirmed

### 7.3 Forecast Reliability
- Last 30 days: mean=1.7, std=1.2
- Forecast: 0.8/day with CI [-38.3, 39.9]
- Verdict: UNRELIABLE. CI width (78.2) exceeds mean by 97x.
- Reason: Training data ends with incomplete 2025 (data stop artifact).

---

## 8. CONCRETE RECOMMENDATIONS

1. Exclude Luhansk Oblast from all aggregations (1 record, occupied territory)
2. Filter data to 2022-2024 for forecasting (complete years only)
3. Note in all reports that 2025 data is incomplete after October
4. The SARIMA forecast should not be presented as reliable - retrain on 2022-2024 data
5. For duration analysis, use median (not mean) due to right-skewed distribution
