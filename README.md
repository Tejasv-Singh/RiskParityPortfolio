# Risk Parity Portfolio Construction
Project Overview
This project involves constructing and analyzing two types of portfolios using the Riskfolio-Lib library in Python:

Equally Weighted Portfolio: All assets have equal weights.
Risk Parity Portfolio: Each asset contributes equally to the overall portfolio risk.
We use historical stock data for selected assets to optimize the portfolios and compare their performance based on risk and return metrics. Through this project, you’ll understand the benefits of risk parity in enhancing diversification and managing portfolio volatility.

# Table of Contents
Project Description
Getting Started
Installation
Data Collection
Portfolio Construction
Equally Weighted Portfolio
Risk Parity Portfolio
Performance Analysis
Visualization
Conclusion
Resources


# Project Description
The goal of this project is to:

Construct and optimize an equally weighted and risk parity portfolio using the Riskfolio-Lib library.
Compare these portfolios based on cumulative returns, annualized return, annualized volatility, Sharpe ratio, and maximum drawdown.
Visualize the portfolio allocations, cumulative returns, and risk-adjusted performance over time.
Key Concepts:
Risk Parity Portfolio: A portfolio in which each asset’s risk contribution is the same. This type of portfolio is designed to maximize diversification by equalizing the risk across assets.
Equally Weighted Portfolio: A naive diversification strategy where each asset has equal weights, regardless of risk or correlation.
Getting Started
Follow these instructions to get a local copy of the project and run the analysis on your system.

Prerequisites
Python 3.x
Jupyter Notebook or any Python IDE
Familiarity with financial data and portfolio optimization concepts
Installation
Install the necessary libraries using pip:

pip install riskfolio-lib pandas numpy matplotlib yfinance seaborn
Data Collection
We will use the yfinance library to fetch historical price data for a set of stocks.

Selected Assets:
Apple Inc. (AAPL)
Microsoft Corporation (MSFT)
Amazon.com Inc. (AMZN)
Johnson & Johnson (JNJ)
JPMorgan Chase & Co. (JPM)
Exxon Mobil Corporation (XOM)
Procter & Gamble Co. (PG)
Google LLC (GOOGL)
Example Python Code:

import yfinance as yf

# Define the list of tickers
tickers = ['AAPL', 'MSFT', 'AMZN', 'JNJ', 'JPM', 'XOM', 'PG', 'GOOGL']

# Define the time period
start_date = '2018-01-01'
end_date = '2023-12-31'

# Fetch adjusted closing prices
prices = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
Portfolio Construction
Equally Weighted Portfolio
Create a portfolio with equal allocation to each asset:

import pandas as pd

# Number of assets
num_assets = len(tickers)

# Equal weights
equal_weights = pd.Series([1/num_assets] * num_assets, index=tickers)
Risk Parity Portfolio
Use Riskfolio-Lib to construct a risk parity portfolio:


import riskfolio as rp

# Create a Portfolio object
port = rp.Portfolio(returns=returns)

# Estimate the mean and covariance
port.assets_stats(method_mu='hist', method_cov='hist')

# Perform Risk Parity optimization
risk_parity_weights = port.optimization(model='RiskParity')
Performance Analysis
Analyze and compare the performance metrics of both portfolios.

Performance Metrics:
Cumulative Returns
Annualized Return
Annualized Volatility
Sharpe Ratio
Maximum Drawdown

# Calculate daily portfolio returns
equal_portfolio_returns = returns.dot(equal_weights)
risk_parity_portfolio_returns = returns.dot(risk_parity_weights)
Visualization
1. Portfolio Allocation Pie Charts

import matplotlib.pyplot as plt

# Plot Equally Weighted Portfolio
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
equal_weights.plot.pie(autopct='%.2f%%', startangle=90)
plt.title('Equally Weighted Portfolio Allocation')

# Plot Risk Parity Portfolio
plt.subplot(1, 2, 2)
risk_parity_weights.plot.pie(autopct='%.2f%%', startangle=90)
plt.title('Risk Parity Portfolio Allocation')

plt.tight_layout()
plt.show()
2. Cumulative Returns Comparison

import seaborn as sns

# Combine cumulative returns into a DataFrame
cumulative_returns = (1 + portfolio_returns).cumprod()

# Plot cumulative returns
plt.figure(figsize=(10, 6))
sns.lineplot(data=cumulative_returns)
plt.title('Cumulative Returns Comparison')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend(loc='best')
plt.show()
3. Rolling Sharpe Ratio

rolling_window = 252  # 1 year

# Calculate rolling Sharpe Ratio
rolling_sharpe_equal = (equal_portfolio_returns.rolling(window=rolling_window).mean() / 
                        equal_portfolio_returns.rolling(window=rolling_window).std()) * np.sqrt(252)

rolling_sharpe_risk = (risk_parity_portfolio_returns.rolling(window=rolling_window).mean() / 
                       risk_parity_portfolio_returns.rolling(window=rolling_window).std()) * np.sqrt(252)

# Combine into DataFrame
rolling_sharpe = pd.DataFrame({
    'Equally Weighted': rolling_sharpe_equal,
    'Risk Parity': rolling_sharpe_risk
})

# Plot rolling Sharpe Ratio
plt.figure(figsize=(10, 6))
sns.lineplot(data=rolling_sharpe)
plt.title('Rolling Sharpe Ratio (1-Year Window)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend(loc='best')
plt.show()

# Conclusion
This project illustrates the construction of a risk parity portfolio and compares it with a traditional equally weighted portfolio. The risk parity approach provides better risk distribution across assets, which can lead to more stable returns and potentially improved performance in various market conditions.

# Resources
Riskfolio-Lib Documentation: [Riskfolio-Lib Docs](https://riskfolio-lib.readthedocs.io/en/latest/)
Riskfolio-Lib GitHub Repository: [Riskfolio-Lib GitHub](https://github.com/dcajasn/Riskfolio-Lib)
yfinance Documentation: [yfinance Docs](https://pypi.org/project/yfinance/)
