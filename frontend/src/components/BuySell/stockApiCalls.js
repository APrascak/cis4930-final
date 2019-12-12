import * as url from './stockApiUrls'
import axios from 'axios';

export  function buyStocks(url, user, amnt){
    return axios
          .get(url + '/buy/' + user+ "/"+amnt )
          .then( res => {console.log('in buy stock res', res); return getStockPrice(url)} )
          .catch(function (error) {
            console.log(error);
          });
}
 
export  function sellStocks(url, user, amnt){
  return axios
        .get(url + '/sell/' + user+ "/"+amnt )
        .then( res => { 
          console.log('res sell ', res)
          if(res.data === "Sorry you do not own enough stocks to sell that amount." || res.data === "Error: insufficient user inventory." || res.data === "insufficient stocks"){
              return "Bad sell amount";
          }
          else{
            return getStockPrice(url);
          }
        } )
        .catch(function (error) {
          console.log(error);
        });
}

export function getStockPrice(url){
    return axios
          .get(url + "/getStockPrice" , {
            method: 'GET',
           })
          .then(
            response => {
              return response.data.stock_price;
            }
          )
          .catch(function (error) {
            console.log(error);
          });
}

export  function getStockAmnt(url, user) {
    return axios
            .get(url + '/getUserHoldings/' +user, {
              method: 'GET',
             })
            .then(response => response.data.shares)
  }