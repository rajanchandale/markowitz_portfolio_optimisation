from flask import Flask, request, jsonify
from flask_cors import CORS

import get_tickers
import markowitz_optimiser as mpt_opt

app = Flask(__name__)
CORS(app) # Enables Cross-Origin Resource Sharing


@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Endpoint to search tickers and company names based on a query

    Parameters:
         - q (str): The search query

     Returns:
         - JSON: A list of matching tickers and company names
    """
    if request.method == 'GET':
        query = request.args.get('q') # Extract the search query from the request arguments
        tickers = get_tickers.get_all_tickers()

        # Filter tickers based on the search query
        results = [ticker for ticker in tickers if query.upper() in ticker['Ticker']
                   or query.upper() in ticker['Company'].upper()]

        return jsonify(results) # Return results as a JSON response


@app.route("/optimise", methods=["POST"])
def optimise():
    """
    Endpoint to optimise a given portfolio using the Markowitz Portfolio Theory

    Parameters:
        - portfolio (list): A list of tickers to be optimised

    Returns:
        - JSON: Contains the optimised portfolio and efficient frontier
    """
    # Extract tickers from the request data
    tickers = request.json['portfolio']
    tickers_in_portfolio = sorted([ticker['Ticker'] for ticker in tickers])

    # Fetch historical data for the tickers
    historical_data = mpt_opt.get_historical_data(tickers_in_portfolio)
    historical_market_data = mpt_opt.get_market_data()

    # Calculate expected returns for the portfolio
    expected_returns = mpt_opt.calculate_expected_portfolio_return(tickers_in_portfolio, historical_data, historical_market_data)

    # Compute the covariance matrix for the tickers
    cov_matrix = historical_data['Adj Close'].pct_change().cov()

    # Fetch the risk-free rate
    risk_free_rate = mpt_opt.get_risk_free_rate()

    # Optimise the portfolio for maximum Sharpe Ratio
    optimal_weights, optimal_return, optimal_volatility = mpt_opt.maximise_sharpe_ratio(expected_returns, cov_matrix, risk_free_rate)

    # Optimise the portfolio for minimum variance
    minimum_variance_weights, minimum_variance_return, minimum_variance_volatility = mpt_opt.minimise_portfolio_variance(expected_returns, cov_matrix)

    # Update tickers with calculated optimal and minimum variance weights
    num_assets = len(tickers)
    for asset in range(num_assets):
        tickers[asset]['Optimal Weight'] = f"{round(optimal_weights[asset]*100, 1)}%"
        tickers[asset]['Minimum Variance Weight'] = f"{round(minimum_variance_weights[asset]*100, 1)}%"

    # Generate the efficient frontier
    ef = mpt_opt.generate_efficient_frontier(expected_returns, optimal_return, optimal_volatility, minimum_variance_return,
                                             minimum_variance_volatility, risk_free_rate, cov_matrix)

    # Prepare the response data
    response = {
        "portfolio": tickers,
        "ef": ef,
        "optimal": {"risk": optimal_volatility, "return": optimal_return},
        "min_variance": {"risk": minimum_variance_volatility, "return": minimum_variance_return}
    }

    return response


if __name__ == '__main__':
    # Entry point
    app.run(debug=True) # Start Flask app in debug mode
