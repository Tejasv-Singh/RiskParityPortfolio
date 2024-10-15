import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import riskfolio as rp

# 1. Data Collection
tickers = ['AAPL', 'MSFT', 'AMZN', 'JNJ', 'JPM', 'XOM', 'PG', 'GOOGL']
start_date = '2018-01-01'
end_date = '2023-12-31'
prices = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

# 2. Data Processing
returns = prices.pct_change().dropna()

# 3. Equally Weighted Portfolio
num_assets = len(tickers)
equal_weights = pd.Series([1/num_assets]*num_assets, index=tickers)

# 4. Risk Parity Portfolio
port = rp.Portfolio(returns=returns)
port.assets_stats(method_mu='hist', method_cov='hist')
risk_parity_weights = port.optimization(model='RiskParity')

# 5. Performance Analysis
def portfolio_return(weights, returns):
    return returns.dot(weights)

equal_portfolio_returns = portfolio_return(equal_weights, returns)
risk_parity_portfolio_returns = portfolio_return(risk_parity_weights, returns)

portfolio_returns = pd.DataFrame({
    'Equally Weighted': equal_portfolio_returns,
    'Risk Parity': risk_parity_portfolio_returns
})

cumulative_returns = (1 + portfolio_returns).cumprod()

def performance_metrics(returns):
    metrics = {}
    metrics['Cumulative Return'] = (1 + returns).prod() - 1
    metrics['Annualized Return'] = returns.mean() * 252
    metrics['Annualized Volatility'] = returns.std() * np.sqrt(252)
    metrics['Sharpe Ratio'] = metrics['Annualized Return'] / metrics['Annualized Volatility']
    metrics['Maximum Drawdown'] = (returns.cumprod().cummax() - returns.cumprod()).max()
    return metrics

metrics_equal = performance_metrics(equal_portfolio_returns)
metrics_risk_parity = performance_metrics(risk_parity_portfolio_returns)

metrics_df = pd.DataFrame({
    'Equally Weighted': metrics_equal,
    'Risk Parity': metrics_risk_parity
})

print(metrics_df)

# 6. Visualization

# A. Portfolio Allocation Pie Charts
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
equal_weights.plot.pie(autopct='%.2f%%', startangle=90)
plt.title('Equally Weighted Portfolio Allocation')

plt.subplot(1, 2, 2)
risk_parity_weights.plot.pie(autopct='%.2f%%', startangle=90)
plt.title('Risk Parity Portfolio Allocation')

plt.tight_layout()
plt.show()

# B. Cumulative Returns Comparison
plt.figure(figsize=(10, 6))
sns.lineplot(data=cumulative_returns)
plt.title('Cumulative Returns Comparison')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend(loc='best')
plt.show()

# C. Rolling Sharpe Ratio
rolling_window = 252  # 1 year
rolling_sharpe_equal = (equal_portfolio_returns.rolling(window=rolling_window).mean() / 
                        equal_portfolio_returns.rolling(window=rolling_window).std()) * np.sqrt(252)
rolling_sharpe_risk = (risk_parity_portfolio_returns.rolling(window=rolling_window).mean() / 
                       risk_parity_portfolio_returns.rolling(window=rolling_window).std()) * np.sqrt(252)

rolling_sharpe = pd.DataFrame({
    'Equally Weighted': rolling_sharpe_equal,
    'Risk Parity': rolling_sharpe_risk
})

plt.figure(figsize=(10, 6))
sns.lineplot(data=rolling_sharpe)
plt.title('Rolling Sharpe Ratio (1-Year Window)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend(loc='best')
plt.show()
