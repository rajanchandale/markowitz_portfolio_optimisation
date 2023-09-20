import { useState } from 'react';
import Autosuggest from 'react-autosuggest';
import axios from 'axios';

import './StockInput.css';

function StockInput({ onStockSelected }){

    const [value, setValue] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [selectedStock, setSelectedStock] = useState(null);

    const onChange = (event, { newValue }) => {
        setValue(newValue);
    }

    const onSuggestionsFetchRequested = async ({ value }) => {

        if (typeof value === 'string' && value.trim() !== ""){
            try{
                const response = await axios.get(`http://localhost:5000/?q=${value}`);
                console.log("Server response: ", response.data);
                let data = Array.isArray(response.data) ? response.data : [];
                setSuggestions(data);
            } catch (err) {
                console.error("Failed to fetch or parse response data", err);
            }
        }

    };

    const onSuggestionsClearRequested = () => {
        setSuggestions([]);
    };

    const getSuggestionValue = suggestion => `${suggestion.Company} (${suggestion.Ticker})`;

    const renderSuggestion = suggestion => (
        <div>
            {suggestion.Company} ({suggestion.Ticker})
        </div>
    );

    const inputProps = {
        placeholder: "Type a stock ticker",
        value,
        onChange: onChange
    }

    const handleAddStock = () => {
        console.log("TRIGGERED")
        console.log(selectedStock);
        console.log("Suggestions: ", suggestions);
        console.log("Current Value: ", value);
        if (selectedStock){
            onStockSelected(selectedStock);
            setSelectedStock(null);
        }
    }

    return (

        <div className = "stock-input-container">
            <Autosuggest
                suggestions={suggestions}
                onSuggestionSelected={(event, { suggestion }) => setSelectedStock(suggestion)}
                onSuggestionsFetchRequested={onSuggestionsFetchRequested}
                onSuggestionsClearRequested={onSuggestionsClearRequested}
                getSuggestionValue={getSuggestionValue}
                renderSuggestion={renderSuggestion}
                inputProps={inputProps}
            />
            <button onClick = {handleAddStock}>Add Stock</button>
        </div>

    );

}

export default StockInput;