## data_pipline
This parts covers the entire pipeline from data acquisition to pre-training, providing detailed analysis and visualization for each step. The example will use SPX stock price.

### Download the data
```bash
python3 download_data.py --ticker ^GSPC --period max --interval 1d
```
#### ticker

Specifies the financial instrument to download.

^GSPC — S&P 500 Index

^N225 — Nikkei 225 Index

SPY — S&P 500 ETF

AAPL — Apple Inc. stock


#### interval
Defines the time frequency of the downloaded data.

1d — Daily data, Maximum available history

1wk — Weekly data, Maximum available history

1mo — Monthly data, Maximum available history

1h — Hourly data, Last 730 days

5m — 5-minute data, Last 60 days

2m — 1-minute data, Last 60 days

1m — 1-minute data, Last 7 days

The downloaded data will be saved under `raw_data/`, and all variables will be visualized and stored in `raw_figures/`. 

![SPX Plot](raw_data/raw_figures/GSPC_max_1d/all_variables.png)

**Figure 1.** Daily OHLCV variables of the S&P 500 Index. The Close/High/Low/Open prices appear very similar while the volume exhibits different.


### Analysis the data
```bash
python3 data_analysis.py --input raw_data/GSPC_max_1d.csv --out_dir analysis/GSPC_1d
```
The analysis results will be saved at analysis/GSPC_1d. 

| Variable    | Count  | Mean      | Std       | Min  | 1%   | 5%   | 50%    | 95%     | 99%     | Max     | Skew  | Kurtosis |
|------------|--------|----------|----------|------|------|------|--------|----------|----------|----------|--------|----------|
| Adj_Close  | 24651  | 723.39   | 1236.89  | 4.40 | 7.70 | 10.07| 103.53 | 3807.70 | 5925.29 | 6978.60 | 2.53   | 6.73     |
| Close      | 24651  | 723.39   | 1236.89  | 4.40 | 7.70 | 10.07| 103.53 | 3807.70 | 5925.29 | 6978.60 | 2.53   | 6.73     |
| High       | 24651  | 727.40   | 1243.20  | 4.40 | 7.70 | 10.07| 104.37 | 3838.19 | 5955.84 | 7002.28 | 2.53   | 6.71     |
| Low        | 24651  | 718.82   | 1229.64  | 4.40 | 7.70 | 10.07| 102.68 | 3782.19 | 5872.95 | 6963.46 | 2.53   | 6.75     |
| Open       | 24651  | 723.25   | 1236.69  | 4.40 | 7.70 | 10.07| 103.54 | 3810.70 | 5920.21 | 7002.00 | 2.53   | 6.73     |
| Volume     | 24651  | 9.68e8   | 1.68e9   | 0.00 | 0.00 | 0.00 | 2.21e7 | 4.57e9  | 6.28e9  | 1.15e10 | 1.75   | 2.18     |
<p align="center">
  <b>Table 1.</b> Descriptive Statistics (GSPC_1d)
</p>>
