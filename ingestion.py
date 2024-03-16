
import requests
import yfinance as yf

import numpy as np
import pandas as pd

def ingest_training_df(ticker = 'EURUSD=X'):

    df = yf.download(ticker)
    df.columns = df.columns.str.lower()
    df['target'] = df['close'].shift(-1)

    df['action'] = (df['target'] > df['close']).astype(int)
    df = df[['open', 'high', 'low', 'close', 'target','action']]
    df.dropna(inplace=True)

    # read data to safe location
    df.to_csv(f'data/{ticker}_{df.index.min().date()}:{df.index.max().date()}.csv')

    return df



df = ingest_training_df()

predictors = df.columns[~df.columns.isin(['target','action']) ]

def pct_diff(old, new):
    return (new - old) / old

def compute_rolling(df, horizon, col):
    label = f"rolling_{horizon}_{col}"
    df[label] = df[col].rolling(horizon).mean()
    df[f"{label}_pct"] = pct_diff(df[label], df[col])
    return df


rolling_horizons = [7, 14]
for horizon in rolling_horizons:
    for col in predictors.tolist():
        df = compute_rolling(df, horizon, col)

def expand_mean(df):
    return df.expanding(1).mean()

for col in predictors.tolist():
    df[f"month_avg_{col}"] = df[col].groupby(df.index.month, group_keys=False).apply(expand_mean)
    df[f"day_avg_{col}"] = df[col].groupby(df.index.day_of_year, group_keys=False).apply(expand_mean)


df.to_csv(f'features/{df.index.min().date()}:{df.index.max().date()}.csv')
