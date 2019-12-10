import * as url from './stockApiUrls'
import axios from 'axios';

export  function buyStocks(url, user, amnt){
    axios
          .get(url + '/buy/' + user+ "/"+amnt )
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
}

export  function sellStocks(url, user, amnt){
  axios
        .get(url + '/sell/' + user+ "/"+amnt )
        .then(function (response) {
          console.log(response);
        })
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