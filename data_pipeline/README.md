## data_pipline
This parts covers the entire pipeline from data acquisition to pre-training, providing detailed analysis and visualization for each step

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

![SPX Plot](raw_figures/GSPC_max_1d/all_variables.png)
