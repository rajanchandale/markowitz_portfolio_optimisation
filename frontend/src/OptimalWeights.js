import React from 'react';

import './OptimalWeights.css'

function OptimalWeights({ stocks }){
    console.log("STOCKS: ", stocks)
    return (

        <div className = "optimal-weights-section">
            <h2>Optimal Weights</h2>
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Ticker</th>
                        <th>MPT Optimal Weight</th>
                    </tr>
                </thead>
                <tbody>
                    {stocks.map(stock => (
                        <tr key = {stock.Ticker}>
                            <td>{stock.Company}</td>
                            <td>{stock.Ticker}</td>
                            <td>{stock['Optimal Weight']}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>

    );

}

export default OptimalWeights;