import React from 'react';
import './MinimumVarianceWeights.css';

function MinimumVarianceWeights({ stocks }){

    return(

        <div className = "minimum-variance-weights-section">
            <h2>Minimum Variance Weights</h2>
            <table>
                <thead>
                    <tr>
                        <th>Company</th>
                        <th>Ticker</th>
                        <th>Min. Variance Weight</th>
                    </tr>
                </thead>
                <tbody>
                    {stocks.map(stock => (
                        <tr key = {stock.Ticker}>
                            <td>{stock.Company}</td>
                            <td>{stock.Ticker}</td>
                            <td>{stock['Minimum Variance Weight']}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>

    );

}

export default MinimumVarianceWeights;