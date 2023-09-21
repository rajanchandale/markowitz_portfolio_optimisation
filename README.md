# Markowitz Portfolio Optimisation

An application that applies Modern Portfolio Theory principles to optimise a portfolio based on the Sharpe Ratio whilst also generating the efficient frontier to help visualise risk-return trade-offs. 

This tool optimises portfolio composition using techniques like CAPM and Sharpe Ratio maximisation. It generates an efficient frontier showing minimised variance weightings for various returns. With a React JS frontend, users get real-time ticker suggestions and can see weights for optimal and minimum variance portfolios. A D3 JS chart visually represents the efficient frontier, color-coding portfolios to indicate their balance of risk and reward.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Features

- **Efficient Frontier Generation:**
    - Offers a graphical representation of the portfolio which minimises risk for a range of return targets, allowing users to understand the risk vs reward dynamics

- **Advanced Financial Calculations:**
    - **CAPM for Expected Returns:**
  
        - Evaluates potential returns on an investment relative to its systematic risk
    - **Sharpe Ratio Maximisation:**
        - Determine's the portfolio's return relative to its volatility. The portfolio composition which maximises the Sharpe Ratio is deemed to be the optimal portfolio
    - **Unlevered Beta Values:**
        - Measures the volatility of the investment without the impact of its financial leverage

- **Real-time Stock Ticker Suggestions:**
    - As users type, stock tickers from both the S&P 500 and FTSE100 are suggested to the user, aiding decision-making and allowing for greater accuracy and consistency

- **D3 JS Visualisation:**
    - An interactive visual map of the efficient frontier. A colour gradient is used to distinguish portfolios based on their ability to balance risk and return by evaluating sharpe ratios.

## Technologies Used

- **Python** is used to empower the backend logic and financial computations
- **Flask** serves as the application's backend API
- **React JS** is used to drive the dynamic frontend
- **D3 JS** leveraged for data visualisation

## Prerequisites

Ensure you have the following installed on your local machine:
- **Python3**
- **Node.js & npm**

## Installation

**1. Clone the Repository:**
```
git clone https://github.com/rajanchandale/markowitz_portfolio_optimisation.git
```

**2. Set Up a Virtual Environment:**
```
python3 -m venv env
source env/bin/activate
```

**3. Install the Required Packages:**
```
pip install -r requirements.txt
```

**4. Navigate to the Frontend Directory and Install Node Modules:**
```
cd frontend
npm install
```

## Usage

**1. Start the Backend Server:**
```
python main.py
```

**2. Start the Frontend Development Server:**
```
cd frontend
npm start
```

Visit http://localhost:3000 in your browser to access the Markowitz Portfolio Optimisation tool
