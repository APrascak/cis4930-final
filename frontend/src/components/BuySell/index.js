
import React, { useState, useEffect } from 'react';
import useForm from 'react-hook-form'
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';
import * as stockApi from './stockApiCalls'
import * as url from './stockApiUrls'
import AddFunds from '../AddFunds';

const BuySell = (props) => {
	
	const [stockPinPrice, setPinStockPrice] = useState( [] );
	const [stockAxpPrice, setAxpStockPrice] = useState( [] );
	const [stockUberPrice, setUberStockPrice] = useState( [] );
	const [stockSnapPrice, setSnapStockPrice] = useState( [] );
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    const [axpAmnt, setAxpAmnt] = useState( [] );
    const [uberAmnt, setUberAmnt] = useState([]);
    const [snapAmnt, setSnapAmnt] = useState([]);

    useEffect(() => {
	  stockApi.getStockPrice(url.PINS).then(response => setPinStockPrice(response))
	  stockApi.getStockPrice(url.AXP).then(response => setAxpStockPrice(response))
	  //stockApi.getStockPrice(url.SNAP).then(response => setPinStockPrice(response))
	  stockApi.getStockPrice(url.UBER).then(response => setUberStockPrice(response))
      stockApi.getStockAmnt(url.PINS ,props.accountId).then(response => setPinsAmnt(response));
      stockApi.getStockAmnt(url.AXP ,props.accountId).then(response => setAxpAmnt(response));
      //stockApi.getStockAmnt(url.SNAP ,props.accountId).then(response => setSnapAmnt(response));
      stockApi.getStockAmnt(url.UBER ,props.accountId).then(response => setUberAmnt(response));
    },);


    function buySell(values, url){
        if(values.action == "buy"){ 
            stockApi.buyStocks(url, props.accountId, values.amnt)
        }
        else{ 
            stockApi.sellStocks(url, props.accountId, values.amnt)
        }
    }

	function manageFunds(values, price) {
		if(values.action == "buy"){ 
			props.firebase.users().doc(props.accountId).set({
           		Money: (props.money - (price * values.amnt)) //or whatever money stockAccount starts off with
			})
        }
        else{ 
			props.firebase.users().doc(props.accountId).set({
           		Money: (props.money + (price * values.amnt)) //or whatever money stockAccount starts off with
			})
        }
	}


    const {register, handleSubmit} = useForm();
    const onSubmit = (values) => {
		if(values.stock === "PINS") (
			buySell(values, url.PINS)
		) 
		if(values.stock === "PINS") (
			manageFunds(values, stockPinPrice)
		)
		if(values.stock === "AXP") (
			buySell(values, url.AXP)
		) 
		if(values.stock === "AXP") (
			manageFunds(values, stockAxpPrice)
		)  
		if(values.stock === "UBER") (
			buySell(values, url.UBER)
		) 
		if(values.stock === "UBER") (
			manageFunds(values, stockUberPrice)
		) 
		if(values.stock === "SNAP") (
			buySell(values, url.SNAP)
		) 
		if(values.stock === "SNAP") (
			manageFunds(values, stockSnapPrice)
		) 
    }

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h3>PINS Stock Amount: {pinsAmnt}, AXP Stock Amount: {axpAmnt}, 
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
				<AddFunds money={props.money} accountId = {props.accountId}></AddFunds>

            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(BuySell);