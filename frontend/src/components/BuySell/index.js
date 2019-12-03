
import React, { useState, useEffect } from 'react';
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

const BuySell = (props) => {
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
          .get("https://pinterestservice.appspot.com/getUserHoldings/"+props.accountId, {
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
        buyStocks( props.accountId, inputs.buyAmnt);
    }

    const handleInputChange = (event) => {
        event.persist();
        setInputs(inputs => ({...inputs, [event.target.name]: event.target.value}));
    }

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h1>Pinterest Stock Amount: {pinsAmnt} , stock value = {price} </h1>
                <form onSubmit = {handleSubmit} >
                    Buy Stocks
                    <input onChange={handleInputChange} value={inputs.buyAmnt} type="number" name="buyAmnt" min="1" />
                    <input type="submit" />
                </form>
            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(BuySell);