import React, { useState } from 'react';
import StockInput from './StockInput';
import OptimalWeights from './OptimalWeights';
import MinimumVarianceWeights from './MinimumVarianceWeights';
import EfficientFrontier from './EfficientFrontier';
import axios from 'axios';

import './UserPortfolio.css'

function UserPortfolio(){

    const [portfolio, setPortfolio] = useState([]);
    const [efficientFrontierData, setEfficientFrontierData] = useState([]);
    const [optimalPortfolio, setOptimalPortfolio] = useState({});
    const [minVariancePortfolio, setMinVariancePortfolio] = useState({});
    const [isOptimising, setIsOptimising] = useState(false);

    function addStock(stock){
        if (!portfolio.some(s => s.Ticker === stock.Ticker)){
            setPortfolio([...portfolio, stock]);
        }
    }

    function removeStock(tickerToRemove){
        setPortfolio(portfolio.filter(stock => stock.Ticker !== tickerToRemove));
    }

    async function optimisePortfolio(){
        setIsOptimising(true);
        try{
            const response = await axios.post('http://localhost:5000/optimise', { portfolio });
            console.log("RESPONSE RAJAN: ", response)
            let response_data = response.data;
            setPortfolio(response_data.portfolio);
            setEfficientFrontierData(response_data.ef);
            setOptimalPortfolio(response_data.optimal);
            setMinVariancePortfolio(response_data.min_variance);
            console.log("OPTIMISE RESPONSE: ", response.data);
            console.log("OPTIMISE RESPONSE PORTFOLIO: ", portfolio)
        } catch (error) {
            console.error("Error Optimising The Portfolio", error);
        } finally {
            setIsOptimising(false);
        }
    }

    return (
        <div>
            <StockInput onStockSelected={addStock} />
            <div className = "portfolio-container">
                <div className="portfolio">
                    <h2>My Portfolio</h2>
                    <ul>
                        {portfolio.map(stock => (
                            <li key = {stock.Ticker}>
                                {stock.Company} ({stock.Ticker})
                                <button onClick={() => removeStock(stock.Ticker)}>Remove</button>
                            </li>
                        ))}
                    </ul>
                </div>
                <button
                    className={`optimise ${isOptimising ? 'optimising' : ''}`}
                    onClick={optimisePortfolio}
                    disabled={isOptimising}
                >
                    {isOptimising ? "Optimising ..." : "Optimise"}
                </button>
            </div>
            <OptimalWeights stocks={portfolio} />
            <MinimumVarianceWeights stocks={portfolio} />
            <EfficientFrontier
                data = {efficientFrontierData}
                optimal = {optimalPortfolio}
                minVariance = {minVariancePortfolio}
            />
        </div>
    );

}

export default UserPortfolio;