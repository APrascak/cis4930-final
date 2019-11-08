#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#hi

from flask import Flask
app = Flask(__name__) 
import requests

def obsGetAvailableStocks():
    # call db
    return 1
    
def obsBuyAdditionalStocks():
    # add additional stocks
    return 1
    
def obsSellStocks():
    # subtract amount that user buys
    return 1


def getPriceFromTradier():
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
    params={'symbols': 'PINS,VXX190517P00016000', 'greeks': 'false'},
    headers={'Authorization': 'Bearer uZOWMJ0Hh2jcz2g9GE2Xa9YNPhMC', 'Accept': 'application/json'})

    resp_json = response.json()
    lastPrice = resp_json["quotes"]["quote"]["last"]
    return lastPrice

@app.route("/",) 
def index():
    return "Welcome to Python Server"

@app.route("/test",) 
def test():
    return " to Python Server"

@app.route("/getStockPrice",)
def getStockPrice():
    price = getPriceFromTradier()
    return str(price)

@app.route("/buy/<userToken>/<int:amount>")
def buyStocks(userToken, amount):
    price = getPriceFromTradier()
    log = userToken + " bought " + str(amount) + " stocks for " + str(amount * price) + " total."
    return log

@app.route("/sell/<userToken>/<int:amount>")
def sellStocks(userToken, amount):
    price = getStockPrice()
    log = userToken + " bought " + str(amount) + " stocks for " + price + " each."
    return log

if __name__ == "__main__":
    app.run(debug=True)
#
