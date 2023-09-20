import pandas as pd


def get_ftse_100_tickers():
    """
    Fetches the tickers and company names of the FTSE 100 index from its Wikipedia page
    The FTSE 100 lists the 100 largest UK companies by market capatilisation

    Returns:
        - list of dicts: A list where each dictionary contains the company name and its ticker
    """
    # Fetches the tables from the FTSE 100 Wikipedia page
    table = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')
    # Selects the appropriate table containing the company and ticker information
    df = table[4]
    data = df[['Company', 'Ticker']].to_dict('records')

    return data


def get_sp500_tickers():
    """
    Fetches the tickers and company names of the S&P 500 index from its Wikipedia page
    The S&P 500 lists 500 major US companies

    Returns:
        - list of dicts: A list where each dictionary contains the company name and its ticker
    """
    # Fetches the tables from the S&P 500 Wikipedia page
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # Selects the first table containing the company name and ticker information
    df = table[0]
    data = df[['Security', 'Symbol']].rename(columns={'Security': 'Company', 'Symbol': 'Ticker'}).to_dict('records')

    return data


def get_all_tickers():
    """
    Combines the tickers from the FTSE 100 and S&P 500 indices, removes duplicates, and sorts them by ticker.

    Returns:
        - list of dicts: A sorted list where each dictionary contains the company name and its ticker
    :return:
    """
    sp500_tickers = get_sp500_tickers()
    ftse100_tickers = get_ftse_100_tickers()

    # Combines the tickers from both FTSE 100 & S&P 500
    all_tickers = sp500_tickers + ftse100_tickers
    # Removes duplicate tickers using dictionary comprehension
    unique_data = {item['Ticker']: item for item in all_tickers}.values()

    # Sorts the list of dictionaries by ticker name
    return sorted(unique_data, key=lambda x: x['Ticker'])

