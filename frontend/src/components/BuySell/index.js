
import React, { useState, useEffect } from 'react';
import useForm from 'react-hook-form'
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';
import * as stockApi from './stockApiCalls'
import * as url from './stockApiUrls'
import Test from './test'
import AddFunds from '../AddFunds';

const BuySell = (props) => {
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    const [axpAmnt, setAxpAmnt] = useState( [] );
    const [uberAmnt, setUberAmnt] = useState([]);
    const [snapAmnt, setSnapAmnt] = useState([]);

    useEffect(() => {
      stockApi.getStockAmnt(url.PINS ,props.accountId).then(response => setPinsAmnt(response));
      //stockApi.getStockAmnt(url.AXP ,props.accountId).then(response => setPinsAmnt(response));
     // stockApi.getStockAmnt(url.SNAP ,props.accountId).then(response => setPinsAmnt(response));
      stockApi.getStockAmnt(url.UBER ,props.accountId).then(response => setUberAmnt(response));
    },);

    const {register, handleSubmit} = useForm();
    const onSubmit = (values) => {
        console.log(values)
        if( values.action == "buy"){
            if(values.stock == "PINS"){stockApi.buyStocks(url.PINS, props.accountId, values.amnt)};
            if(values.stock == "AXP"){stockApi.buyStocks(url.AXP, props.accountId, values.amnt)};
            if(values.stock == "UBER"){stockApi.buyStocks(url.UBER, props.accountId, values.amnt)};
            if(values.stock == "SNAP"){stockApi.buyStocks(url.SNAP, props.accountId, values.amnt)};
        }
        else{
            if(values.stock == "PINS"){stockApi.sellStocks(url.PINS, props.accountId, values.amnt)};
            if(values.stock == "AXP"){stockApi.sellStocks(url.AXP, props.accountId, values.amnt)};
            if(values.stock == "UBER"){stockApi.sellStocks(url.UBER, props.accountId, values.amnt)};
            if(values.stock == "SNAP"){stockApi.sellStocks(url.SNAP, props.accountId, values.amnt)};
        }
    }

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h3>PINS Stock Amount: {pinsAmnt}, AXP Stock Amount: {axpAmnt} 
                UBER Stock Amount: {uberAmnt}, SNAP Amount: {snapAmnt}
                </h3>

                <form onSubmit = {handleSubmit(onSubmit)} >               
                    <select name="action" ref = {register}>
                          <option value="buy">Buy</option>
                          <option value="sell">Sell</option>
                    </select>

                    <select  name="stock" ref = {register}>
                      <option value="PINS">Pinterest Stock</option>
                      <option value="AXP">American Express Stock</option>
                      <option value="UBER">Uber Stock</option>
                      <option value="SNAP">Snapchat Stock</option>
                    </select>

                    <input  type="number" name="amnt" min="1" ref = {register} />
                    <input type="submit" />
                </form>
                <Test amount = {pinsAmnt} />

				<AddFunds money={props.money} accountId = {props.accountId}></AddFunds>

            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(BuySell);