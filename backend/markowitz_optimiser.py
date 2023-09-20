import numpy as np
import yfinance as yf
import quandl
import datetime
from scipy.optimize import minimize


def get_historical_data(tickers):
    """
    Fetches historical stock data for the provided tickers for the past 5 years

    Parameters:
        - tickers (list): List of stock tickers.

    Returns:
        - DataFrame: Historical data for the provided tickers
    """
    # Define start and end date for the past five years
    start_date = (datetime.datetime.now() - datetime.timedelta(days=5 * 365)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Use yfinance to download historical data for the tickers
    historical_data = yf.download(tickers, start=start_date, end=end_date)

    return historical_data


def calculate_expected_portfolio_return(portfolio, historical_data, historical_market_data):
    """
    Calculates the expected return of a portfolio based on the expected return for each individual investment in the portfolio

    Parameters:
        - portfolio (list): List of stock tickers in the portfolio
        - historical_data (DataFrame): Historical stock data for the portfolio
        - historical_market_data (DataFrame): Historical market data

    Returns:
        - np.array Array of expected returns for each ticker in the portfolio
    """
    expected_returns = [calculate_expected_investment_return(ticker, historical_data, historical_market_data)
                        for ticker in portfolio]

    return np.array(expected_returns)


def calculate_expected_investment_return(ticker, historical_data, historical_market_data):
    """
    Calculate the expected return of an individual investment using the Capital Asset Pricing Model (CAPM)
    Expected Return = Risk-free Rate + Beta * (Market Return - Risk-free Rate)

    Parameters:
        - ticker (str): Stock ticker of the investment
        - historical_data (DataFrame): Historical stock data
        - historical_market_data (DataFrame): Historical market data

    Returns:
        - float: Expected return of the investment
    """
    risk_free_rate = get_risk_free_rate()
    beta = get_beta_value(ticker, historical_data, historical_market_data)
    market_return = get_market_return_rate()

    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)

    return expected_return


def get_risk_free_rate():
    """
    Retrieves the current risk-free rate using QUANDL's FRED/GS5 dataset
    This dataset provides the 5 year Treasury constant maturity rate which is used as the risk-free rate

    Returns:
        - float: Current risk-free rate as a decimal
    """
    quandl.ApiConfig.api_key = "AvdPq6Lw4_VFkatgyqnx"

    data = quandl.get("FRED/GS5", collapse="daily", rows=1)

    rate = data.iloc[0]['Value']

    return rate / 100


def get_beta_value(ticker, historical_data, historical_market_data):
    """
    Calculates the unlevered beta value of a stock ticker using the formula:
    beta = covariance (Asset Returns, Market Returns) / Variance (Market Returns)

    Parameters:
        - ticker (str): Stock ticker
        - historical_data (DataFrame): Historical stock data
        - historical_market_data (DataFrame): Historical market data

    Returns:
        - float: Beta value of the stock
    """
    historical_investment_data = historical_data['Adj Close'][ticker]
    historical_market_data = historical_market_data['Adj Close']

    # Align timeframes for both datasets
    start_date = max(historical_investment_data.index.min(), historical_market_data.index.min())
    end_date = min(historical_investment_data.index.max(), historical_market_data.index.max())

    historical_investment_data = historical_investment_data.loc[start_date:end_date]
    historical_market_data = historical_market_data.loc[start_date:end_date]

    # Compute daily returns for both datasets
    historical_investment_returns = historical_investment_data.pct_change().dropna()
    historical_market_returns = historical_market_data.pct_change().dropna()

    # Calculate beta using covariance and variance
    covariance = np.cov(historical_investment_returns, historical_market_returns)[0][1]
    variance = np.var(historical_market_returns)

    unlevered_beta = covariance / variance

    return unlevered_beta


def get_market_data():
    """
    Fetches historical market data for the S&P 500 for the past 5 years

    Returns:
        - DataFrame: Historical market data for the S&P 500
    """
    # Define start and end date for the past 5 years
    start_date = (datetime.datetime.now() - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    #Download historical data for S&P 500
    market_data = yf.download('^GSPC', start=start_date, end=end_date)

    return market_data


def get_market_return_rate():
    """
    Calculates the annualised market return rate based on the historical market data
    annualised return = [(End price / Start price) ^ (1 / number of years)] - 1

    Returns:
        - float: Annualised market return rate
    """
    market_data = get_market_data()

    start_price = market_data['Adj Close'].iloc[0]
    end_price = market_data['Adj Close'].iloc[-1]

    cumulative_return = (end_price/start_price)-1
    annualised_return = (1 + cumulative_return)**(1/5) - 1

    return annualised_return


def maximise_sharpe_ratio(expected_returns, cov_matrix, risk_free_rate):
    """
    Optimises portfolio weights to maximise Sharpe Ratio
    Sharpe Ratio = (Portfolio Return - Risk-free rate) / Portfolio Std. Deviation

    Parameters:
        - expected_returns (np.array): Array of expected returns for each asset
        - cov_matrix (np.array): Covariance matrix of asset returns
        - risk_free_return (float): Current risk-free rate

    Returns:
        - tuple: Optimal portfolio weights, optimal return, optimal volatility
    """
    num_assets = len(expected_returns)

    def objective(weights):
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std

        return -sharpe_ratio # Negative because the aim is to maximise the Sharpe Ratio

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

    bounds = tuple((0, 1) for asset in range(num_assets))

    initial_weights = [1./num_assets for asset in range(num_assets)]

    solution = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

    if not solution.success:
        raise Exception(solution.message)

    optimal_weights = solution.x
    optimal_return = np.dot(optimal_weights, expected_returns)
    optimal_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))

    return optimal_weights, optimal_return, optimal_volatility


def minimise_portfolio_variance(expected_returns, cov_matrix):
    """
    Optimises the portfolio weights to minimise the overall portfolio variance

    Parameters:
        - expected_returns (np.array): Array of expected returns for each asset
        - cov_matrix (np.array): Covariance matrix of asset returns

    Returns:
        - tuple: Portfolio weights that minimise variance, the corresponding portfolio, and the portfolio risk
    """
    num_assets = len(expected_returns)

    def objective(weights):
        portfolio_variance = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        return portfolio_variance

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

    bounds = tuple((0, 1) for asset in range(num_assets))

    initial_weights = [1./num_assets for asset in range(num_assets)]

    solution = minimize(objective, initial_weights, method='SLSQP', bounds=bounds,
                        constraints=constraints)

    if not solution.success:
        raise Exception(solution.message)

    min_volatility_weights = solution.x
    min_volatility_return = np.dot(min_volatility_weights, expected_returns)
    min_volatility_risk = np.sqrt(np.dot(min_volatility_weights.T, np.dot(cov_matrix, min_volatility_weights)))

    return min_volatility_weights, min_volatility_return, min_volatility_risk


def minimum_variance_for_target_return(target_return, expected_returns, cov_matrix):
    """
    Finds the portfolio with the minimum variance for a given target return

    Parameters:
        - target_return (float): Desired portfolio return
        - expected_returns (float): Array of expected returns for each asset
        - cov_matrix (np.array): Covariance matrix of asset returns

    Returns:
        - tuple: Portfolio risk and the corresponding portfolio weights
    """
    num_assets = len(expected_returns)

    def objective(weights):
        # This function calculates the portfolio variance given weights
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    constraints = (
        {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
        {'type': 'eq', 'fun': lambda weights: np.dot(weights, expected_returns) - target_return}
    )

    bounds = tuple((0, 1) for asset in range(num_assets))

    initial_weights = [1./num_assets for asset in range(num_assets)]

    solution = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

    if not solution.success:
        raise Exception(solution.message)

    return solution.fun, solution.x


def generate_efficient_frontier(expected_returns, optimal_return, optimal_volatility, min_vol_return,
                                min_vol_risk, risk_free_rate, cov_matrix):
    """
    Generates the efficient frontier by calculating the minimum variance for a range of target returns

    The efficient frontier is the set of optimal portfolios that offer the highest expected return for a defined level
    of risk or the lowest risk for a given level of expected return

    Parameters:
        - expected_returns (np.array): Array of expected returns for each asset
        - optimal_returns (float): Return of the portfolio with maximum Sharpe Ratio
        - optimal_volatility (float): Risk of the portfolio with maximum Sharpe Ratio
        - min_vol_return (float): Return of the minimum variance portfolio
        - min_vol_risk (float): Risk of the minimum variance portfolio
        - risk_free_rate (float): Current risk-free rate
        - cov_matrix (np.array): Covariance matrix of asset returns

    Returns:
        - list: List of dictionaries containing 'risk', 'return', and  'sharpe_ratio' for portfolios on the efficient
        frontier
    """
    return_targets = np.linspace(min(expected_returns), max(expected_returns), 5000)
    efficient_frontier_risk = []

    efficient_frontier = []

    for target in return_targets:
        variance, weights = minimum_variance_for_target_return(target, expected_returns, cov_matrix)
        efficient_frontier_risk.append(variance)
        sharpe_ratio = (target-risk_free_rate) / np.sqrt(variance)

        ef_dict = {'risk': variance, 'return': target, 'sharpe_ratio': sharpe_ratio}
        efficient_frontier.append(ef_dict)

    return efficient_frontier

