#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__) 
import requests

@app.route("/",) 
def index():
    return "Welcome to Python Server"

@app.route("/getStockPrice",)
def getStockPrice():
    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
    params={'symbols': 'PINS,VXX190517P00016000', 'greeks': 'false'},
    headers={'Authorization': 'Bearer uZOWMJ0Hh2jcz2g9GE2Xa9YNPhMC', 'Accept': 'application/json'})
  
    resp_json = response.json()
    lastPrice = resp_json["quotes"]["quote"]["last"]
    return str(lastPrice)

if __name__ == "__main__":
    app.run(debug=True)
#
