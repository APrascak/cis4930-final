
import React, { useState, useEffect } from 'react';
import useForm from 'react-hook-form'
import { AuthUserContext, withAuthorization } from '../Session';
import axios from 'axios';
import * as stockApi from './stockApiCalls'
import * as url from './stockApiUrls'
import AddFunds from '../AddFunds';

const BuySell = (props) => {
    const [pinsAmnt, setPinsAmnt] = useState( [] );
    const [axpAmnt, setAxpAmnt] = useState( [] );
    const [uberAmnt, setUberAmnt] = useState([]);
    const [snapAmnt, setSnapAmnt] = useState([]);
    const [accountUpdate, setAccountUpdate] = useState([])

    useEffect(() => {
      stockApi.getStockAmnt(url.PINS ,props.accountId).then(response => setPinsAmnt(response));
      stockApi.getStockAmnt(url.AXP ,props.accountId).then(response => setAxpAmnt(response));
      stockApi.getStockAmnt(url.SNAP ,props.accountId).then(response => setSnapAmnt(response));
      stockApi.getStockAmnt(url.UBER ,props.accountId).then(response => setUberAmnt(response));
    },);


    async function buySell(values, url){
        if(values.action == "buy"){ 
            await stockApi.buyStocks(url, props.accountId, values.amnt).then(res => 
                setAccountUpdate({"action":values.action,"stock":values.stock,"amnt":values.amnt,"price":res}) 
            )
        }
        else{ 
            await stockApi.sellStocks(url, props.accountId, values.amnt).then(res =>{
                console.log("res : ",res)
                if(res === "Bad sell amount") {
                    alert("Sorry, you do not own enough stocks to sell the selected amount")

                }
                else {
                    setAccountUpdate({"action":values.action,"stock":values.stock,"amnt":values.amnt,"price":res})
                } 
             } )
        }
    }

    const {register, handleSubmit} = useForm();
    const onSubmit = (values) => {
        if(values.stock === "PINS"){  buySell(values, url.PINS) };
        if(values.stock === "AXP"){  buySell(values, url.AXP) };
        if(values.stock === "UBER"){ buySell(values, url.UBER) };
        if(values.stock === "SNAP"){  buySell(values, url.SNAP) };
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
				<AddFunds accountUpdate = {accountUpdate} money={props.money} accountId = {props.accountId}></AddFunds>

            </div>
            )}
        </AuthUserContext.Consumer>
    )
};
const condition = authUser => !!authUser;
export default withAuthorization(condition)(BuySell);