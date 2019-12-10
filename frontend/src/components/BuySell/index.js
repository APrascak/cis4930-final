
import React, { useState, useEffect } from 'react';
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';
import * as stockApi from './stockApiCalls'
import * as url from './stockApiUrls'


const BuySell = (props) => {
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    const [axpAmnt, setAxpAmnt] = useState( [] );

    useEffect(() => {
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
                <h3>PINS Stock Amount: {pinsAmnt}, AXP Stock Amount: {axpAmnt} </h3>

                <form onSubmit = {handleSubmit} >               
                    <select name="action">
                          <option value="buy">Buy</option>
                          <option value="sell">Sell</option>
                    </select>

                    <select name="stock">
                      <option value="PINS">Pinterest Stock</option>
                    </select>

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