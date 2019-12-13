
import React, { useState, useEffect } from 'react';
import useForm from 'react-hook-form'
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';
import * as stockApi from './stockApiCalls'
import * as url from './stockApiUrls'
import AddFunds from '../AddFunds';
import { withFirebase } from '../Firebase';
// test

const BuySell = (props) => {
	
	const [stockPinPrice, setPinStockPrice] = useState( [] );
	const [stockAxpPrice, setAxpStockPrice] = useState( [] );
	const [stockUberPrice, setUberStockPrice] = useState( [] );
	const [stockSnapPrice, setSnapStockPrice] = useState( [] );
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    const [axpAmnt, setAxpAmnt] = useState( [] );
    const [uberAmnt, setUberAmnt] = useState([]);
    const [snapAmnt, setSnapAmnt] = useState([]);
    const [acctWorth, setacctWorth] = useState([]);
    const [inValidSell, setinValidSell] = useState(false)
    const [inValidBuy, setinValidBuy] = useState(false)

    useEffect(() => {
       
	  stockApi.getStockPrice(url.PINS).then(response => setPinStockPrice(response))
	  stockApi.getStockPrice(url.AXP).then(response => setAxpStockPrice(response))
	  stockApi.getStockPrice(url.SNAP).then(response => setSnapStockPrice(response))
      stockApi.getStockPrice(url.UBER).then(response => setUberStockPrice(response))
      
      stockApi.getStockAmnt(url.PINS ,props.accountId).then(response => setPinsAmnt(response));
      stockApi.getStockAmnt(url.AXP ,props.accountId).then(response => setAxpAmnt(response));
      stockApi.getStockAmnt(url.SNAP ,props.accountId).then(response => setSnapAmnt(response));
      stockApi.getStockAmnt(url.UBER ,props.accountId).then(response => setUberAmnt(response));

      setacctWorth(( (pinsAmnt*stockPinPrice) + (axpAmnt*stockAxpPrice) + 
      (uberAmnt*stockUberPrice) + (snapAmnt*stockSnapPrice) + props.money) )
    },);

    function buySell(values, url, price){
        if(values.action == "buy"){ 
            let money = (props.money - (price * values.amnt))
            if (money <= 0){
                setinValidBuy(true)  
            }
            else{
                stockApi.buyStocks(url, props.accountId, values.amnt)
                var currentdate = new Date();
                var datetime = currentdate.getDate() + "-"
                                + (currentdate.getMonth()+1)  + "-" 
                                + currentdate.getFullYear() + " @ "  
                if (currentdate.getHours() < 10) {
                datetime += "0" + currentdate.getHours() + ":"
                } else {
                datetime += currentdate.getHours() + ":"
                }
                if (currentdate.getMinutes() < 10) {
                datetime += "0" + currentdate.getMinutes() + ":"
                } else {
                datetime += currentdate.getMinutes() + ":"
                }
                if (currentdate.getSeconds() < 10) {
                datetime += "0" + currentdate.getSeconds()
                } else {
                datetime += + currentdate.getSeconds()
                }
                props.firebase.db.collection('transaction-logs').doc(datetime.toString()).set({
                    "Action": values.action,
                    "Account": props.accountId,
                    "Stock": values.stock,
                    "Amount": values.amnt
                })
                props.firebase.users().doc(props.accountId).set({
                    Money: (props.money - (price * values.amnt)) 
                })
            }
        }
        else{ 
            stockApi.sellStocks(url, props.accountId, values.amnt).then(res =>{
                if(res === "Bad sell amount") {
                    setinValidSell(true);
                }
                else {
                    var currentdate = new Date();
                    var datetime = currentdate.getDate() + "-"
                                    + (currentdate.getMonth()+1)  + "-" 
                                    + currentdate.getFullYear() + " @ "  
                    if (currentdate.getHours() < 10) {
                    datetime += "0" + currentdate.getHours() + ":"
                    } else {
                    datetime += currentdate.getHours() + ":"
                    }
                    if (currentdate.getMinutes() < 10) {
                    datetime += "0" + currentdate.getMinutes() + ":"
                    } else {
                    datetime += currentdate.getMinutes() + ":"
                    }
                    if (currentdate.getSeconds() < 10) {
                    datetime += "0" + currentdate.getSeconds()
                    } else {
                    datetime += + currentdate.getSeconds()
                    }
                    props.firebase.db.collection('transaction-logs').doc(datetime.toString()).set({
                        "Action": values.action,
                        "Account": props.accountId,
                        "Stock": values.stock,
                        "Amount": values.amnt
                    })
                    props.firebase.users().doc(props.accountId).set({
                        Money: (props.money + (price * values.amnt)) 
                    })
                } 
            })     
        }
    }


    const {register, handleSubmit} = useForm();
    const onSubmit = (values) => {
        setinValidSell(false)
        setinValidBuy(false)
		if(values.stock === "PINS") (
			buySell(values, url.PINS, stockPinPrice)
		) 
		if(values.stock === "AXP") (
			buySell(values, url.AXP, stockAxpPrice)
		) 
		if(values.stock === "UBER") (
			buySell(values, url.UBER, stockUberPrice)
		) 
		if(values.stock === "SNAP") (
			buySell(values, url.SNAP, stockSnapPrice)
		) 
    }

    return(
        <AuthUserContext.Consumer>
            {authUser => (
            <div>
                <h2 style ={{color:'blue'}}>Stock Account Net Worth: {acctWorth}</h2>
                <h3>PINS Stock Amount: {pinsAmnt}, AXP Stock Amount: {axpAmnt}, UBER Stock Amount: {uberAmnt}, SNAP Amount: {snapAmnt}</h3>
                <h6 style ={{color:'green'}} >PINS: ${stockPinPrice} AXP: ${stockAxpPrice} UBER: ${stockUberPrice} SNAP: ${stockSnapPrice}</h6>
                <form name = "buySellStocksForm" onSubmit = {handleSubmit(onSubmit)} >               
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

                    <input  type="number" name="amnt" min="1" defaultValue ="1" ref = {register} />
                    <input name = "submitStocks" type="submit" />
                </form>
                <h4 name ="sellError" style ={{color:'red'}} >{inValidSell ? 'Invalid: you cannot sell stocks you do not own' : ''}</h4>
                <h4 name ="buyError" style ={{color:'red'}} >{inValidBuy ? 'Invalid: you do not have enough funds to buy these stocks' : ''}</h4>

				        <AddFunds money={props.money} accountId = {props.accountId}></AddFunds>
            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(BuySell);