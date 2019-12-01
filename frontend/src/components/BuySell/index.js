
import React, { useState, useEffect } from 'react';
import StockAccount from '../StockAcount';
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';


const AccountPage = () => {
    const [data, setData] = useState({ currentStockPrice: 0 });
    
    useEffect(() => {
        axios
          .get("https://pinterestservice.appspot.com/getStockPrice", {
            method: 'GET',
           })
          .then(response => setData(response.data))
          .catch(error => console.log(error));
      }, []);

    

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h1>Account: {authUser.email}</h1>
                <h1>Pinterest Stock Price: </h1>
                <StockAccount data="1"/>
                <StockAccount data="2"/>
                <StockAccount data="3"/>
                <StockAccount data="4"/>
                <StockAccount data="5"/>
            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(AccountPage);