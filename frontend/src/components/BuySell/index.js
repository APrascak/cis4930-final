
import React, { useState, useEffect } from 'react';
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';
import * as stockApi from './stockApiCalls'
import * as url from './stockApiUrls'
import AddFunds from '../AddFunds';


const BuySell = (props) => {
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    useEffect(() => {
      console.log(url.PINS)
      stockApi.getStockAmnt(url.PINS ,props.accountId).then(response => setPinsAmnt(response));
    },);

    const [inputs, setInputs] = useState({});
    const handleSubmit = (event) => {
        if (event) {
          event.preventDefault();
        }
        stockApi.buyStocks(url.PINS,props.accountId, inputs.buyAmnt);
    }

    const handleInputChange = (event) => {
        event.persist();
        setInputs(inputs => ({...inputs, [event.target.name]: event.target.value}));
    }

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h1>Pinterest Stock Amount: {pinsAmnt}  </h1>
                <form onSubmit = {handleSubmit} >
                    Buy Stocks
                    <input onChange={handleInputChange} value={inputs.buyAmnt} type="number" name="buyAmnt" min="1" />
                    <input type="submit" />
                </form>
				<AddFunds money={props.money} accountId = {props.accountId}></AddFunds>
            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(BuySell);