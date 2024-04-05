import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


# Function to collect the data
def ingest_training_df(ticker = 'EURUSD=X'):
    df = yf.download(ticker)
    df.columns = df.columns.str.lower()
    return df

# Function to calculate cumulative returns
def calculate_cumulative_returns(returns):
    cumulative_returns = (1 + returns).cumprod() - 1
    return cumulative_returns

# Function to calculate Sharpe ratio
def calculate_sharpe_ratio(returns):
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    return sharpe_ratio

# Function to calculate maximum drawdown
def calculate_max_drawdown(cumulative_returns):
    rolling_max = cumulative_returns.expanding(min_periods=1).max()
    drawdown = cumulative_returns - rolling_max
    max_drawdown = drawdown.min()
    return max_drawdown

# Function to backtest strategy
def backtest_strategy(data, signal):
    returns = data['close'].pct_change().shift(-1) * signal
    cumulative_returns = calculate_cumulative_returns(returns)
    sharpe_ratio = calculate_sharpe_ratio(returns)
    max_drawdown = calculate_max_drawdown(cumulative_returns)
    return returns, cumulative_returns, sharpe_ratio, max_drawdown

# Function to optimize strategy
def optimize_strategy(data):
    # Implement your optimization logic here
    # This can involve iterating over different parameters of your trading strategy
    # and selecting the combination that maximizes a certain metric, such as Sharpe ratio
    # For simplicity, this function currently returns random parameters
    signal = np.random.choice([-1, 0, 1], size=len(data))
    return signal

# Main function
def main():
    # Load historical forex data
    data = ingest_training_df()
    

    # Optimize strategy
    signal = optimize_strategy(data)
    
    # Backtest optimized strategy
    returns, cumulative_returns, sharpe_ratio, max_drawdown = backtest_strategy(data, signal)
    
    # Print relevant metrics
    print("Sharpe Ratio:", sharpe_ratio)
    print("Max Drawdown:", max_drawdown)
    
    # Generate performance chart
    fig, ax = plt.subplots()
    ax.plot(data.index, cumulative_returns)
    ax.set_title('Cumulative Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Returns')
    plt.show()

if __name__ == "__main__":
    main()
