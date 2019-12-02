
import React, { useState, useEffect } from 'react';
import StockAccount from '../StockAcount';
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';

function buyStocks(user, amnt){
    console.log(amnt);
    axios
          .get('https://pinterestservice.appspot.com/buy/' + user+ "/"+amnt )
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
}

const AccountPage = (props) => {
    const [price, setPrice] = useState( [] );
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    useEffect(() => {
        axios
          .get("https://pinterestservice.appspot.com/getStockPrice", {
            method: 'GET',
           })
          .then(response => setPrice(response.data.stock_price))
          .catch(error => console.log(error));
      }, []);

    useEffect(() => {
        axios
          .get("https://pinterestservice.appspot.com/getUserHoldings/"+props.firebase.auth.currentUser.uid, {
            method: 'GET',
           })
          .then(response => setPinsAmnt(response.data.shares))
          .catch(error => console.log(error));
    }, []);

    const [inputs, setInputs] = useState({});
    const handleSubmit = (event) => {
        if (event) {
          console.log("submit : ",inputs)
          event.preventDefault();
        }
        buyStocks( props.firebase.auth.currentUser.uid, inputs.buyAmnt);
    }

    const handleInputChange = (event) => {
        event.persist();
        setInputs(inputs => ({...inputs, [event.target.name]: event.target.value}));
    }

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h1>Account: {authUser.uid}  </h1>
                <h1>Pinterest Stock Price: {price} </h1>
                <h1>Pinterest Stock Amount: {pinsAmnt} </h1>
                <form onSubmit = {handleSubmit} >
                    Buy Stocks
                    <input onChange={handleInputChange} value={inputs.buyAmnt} type="number" name="buyAmnt" min="1" />
                    <input type="submit" />
                </form>
                <StockAccount data="1"/>
            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(AccountPage);