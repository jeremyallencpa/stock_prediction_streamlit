import numpy as np
import pandas_datareader as web


# Function to generate random weights for Monte Carlo simulations based upon number of stocks entered.
# Total weight will add to 1.
def gen_weights(n):
    weights = np.random.random(n)
    weights = weights / np.sum(weights)
    return weights


# Function to calculate returns based upon weights and log returns.
def calculate_returns(weights, log_rets):
    return np.sum(log_rets.mean()*weights) * 252


# Function to calculate the volatility based upon weights and the log returns covariance.
def calculate_volatility(weights, log_rets_cov):
    annualized_cov = np.dot(log_rets_cov*252, weights)
    vol = np.dot(weights.transpose(), annualized_cov)
    return np.sqrt(vol)


# Function to calculate cumulative portfolio returns based upon tickers, weights, start, and end dates.
def calc_portfolio_cumulative_returns(tickers, weights, start, end):
    price_data = web.DataReader(list(tickers), 'yahoo', start, end)['Adj Close']
    ret_data = price_data.pct_change()[1:]
    weighted_returns = (weights * ret_data)
    port_ret = weighted_returns.sum(axis=1)
    cumulative_ret = (port_ret + 1).cumprod() * 1000
    weighted_returns['Cumulative Returns $1,000'] = cumulative_ret
    weighted_returns['Symbol'] = "Portfolio"
    weighted_returns.reset_index(inplace=True)
    return weighted_returns


# Function to build the portfolio to optimize for the maximum Sharpe ratio.
def portfolio_builder(tickers, start, end):
    # Generate data based upon tickers.
    data = web.DataReader(list(tickers), 'yahoo', start, end)['Adj Close']
    # Set variables for log_rets and log_rets_cov.
    log_rets = np.log(data/data.shift(1))
    log_rets_cov = log_rets.cov()
    # Track Monte Carlo portfolio returns, volatility, and weights
    mc_portfolio_returns = []
    mc_portfolio_vol = []
    mc_weights = []
    # Run 3,000 Monte Carlo simulations with random portfolio weights.
    for sim in range(3000):

        weights = gen_weights(n=len(tickers))
        mc_weights.append(weights)
        sim_returns = calculate_returns(weights, log_rets)
        mc_portfolio_returns.append(sim_returns)
        sim_vol = calculate_volatility(weights, log_rets_cov)
        mc_portfolio_vol.append(sim_vol)
    # Calculate Sharpe Ratios
    mc_sharpe_ratios = np.array(mc_portfolio_returns)/np.array(mc_portfolio_vol)
    # Calculate index position of highest sharpe ratio and return those weights.
    max_sharpe_ratio = np.argmax(mc_sharpe_ratios)
    optimal_weights = mc_weights[max_sharpe_ratio]
    return optimal_weights
