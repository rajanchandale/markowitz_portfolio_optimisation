import { useEffect } from 'react';
import StockInput from './StockInput';
import UserPortfolio from './UserPortfolio';

const Home = () => {

    useEffect(() => {
        alert("DISCLAIMER: This Markowitz Portfolio Optimiser tool is a personal project developed by Rajan Chandale primarily for educational and demonstration purposes. It is built upon certain assumptions and analytical methods, and the results are not guaranteed to be accurate or directly applicable to individual investment scenarios. While it showcases certain financial modelling techniques, users are strongly advised to conduct their own due diligence before making any investment decisions based on the tool's output. This project is an educational exercise and we assume no responsibility for any losses or damages incurred as a result of using this tool.");
    }, []);

    return(

        <UserPortfolio />

    )

}

export default Home;
