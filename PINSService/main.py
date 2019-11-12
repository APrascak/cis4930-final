#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from google.cloud import firestore
import requests
from flask import Flask


db = firestore.Client.from_service_account_json('../../credentials/pinterestservice-firebase-adminsdk-6ubsp-9e03db19db.json')

app = Flask(__name__)


def getUserHoldingsDb(userID):
    doc_ref = db.collection(u'UserHoldings_PINS').document(userID)
    try:
        doc = doc_ref.get()
        return  {"stock_amnt" :(doc.to_dict()['stock_amnt'])}
    except TypeError:
        return 0

def updateUserHoldingsDb(userID, amnt, action):
    currStocks = getUserHoldingsDb(userID)['stock_amnt']
    
    if action == "buy":
        updatedStocks = currStocks + amnt
    else:
        updatedStocks = currStocks - amnt
 
    doc_ref = db.collection(u'UserHoldings_PINS').document(userID)
    doc_ref = doc_ref.set({
            u'stock_amnt': updatedStocks
            })
    return 1

def obsGetAvailableStocks():
    doc_ref = db.collection(u'OBS_holdings').document('FGABKyqIk71Fn8e1n94j')
    try:
        doc = doc_ref.get()
        return  {
                "total_stocks": doc.to_dict()['total_stocks'],
                "cost_to_bank": doc.to_dict()['cost_to_bank']     
                 }
    except TypeError:
        return 0
   
def obsUpdateStockHoldings(amount, action):
    # add or sell additional stocks
    cost = amount * getPriceFromTradier()
    currCostToBank = obsGetAvailableStocks()['cost_to_bank']
    currStocks = obsGetAvailableStocks()['total_stocks']

    if action == "buy":
        updatedCost = currCostToBank - cost
        updatedStocks = currStocks + amount
    else:
        updatedCost = currCostToBank + cost
        updatedStocks = currStocks - amount            
    
    doc_ref = db.collection(u'OBS_holdings').document('FGABKyqIk71Fn8e1n94j')
    doc_ref = doc_ref.set({
            u'total_stocks': updatedStocks,
            u'cost_to_bank': updatedCost
            })
            
    return 1

def getPriceFromTradier():
    try:
        response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                                params={'symbols': 'PINS,VXX190517P00016000', 'greeks': 'false'},
                                headers={'Authorization': 'Bearer uZOWMJ0Hh2jcz2g9GE2Xa9YNPhMC', 'Accept': 'application/json'})
    except requests.exceptions.RequestException as e:
        print("Get stock price request error: ", e)
        
    resp_json = response.json()
    lastPrice = resp_json["quotes"]["quote"]["last"]
    return lastPrice



@app.route("/",) 
def index():
    return "Welcome to Python Server"

@app.route("/getStockPrice",)
def getStockPrice():
    result = {"stock_price": getPriceFromTradier()}
    return result

@app.route("/getUserHoldings/<userID>",) 
def getUser(userID):
    result = {"stock_amnt": getUserHoldingsDb(userID)}
    return result

@app.route("/getOBSHoldings",) 
def getOBS():
    result = {"stock_amnt": obsGetAvailableStocks()}
    return result

@app.route("/buy/<userID>/<int:amount>")
def buyStocks(userID, amount):
    #check bank holdings
    bankholdings = obsGetAvailableStocks()['total_stocks']
    if amount > bankholdings:
        amntNeeded = amount - bankholdings 
        obsUpdateStockHoldings((amntNeeded + 1), "buy")
    # bank sells stocks
    obsUpdateStockHoldings(amount, "sell")
    # user buys stock
    updateUserHoldingsDb(userID, amount, "buy")
    return "bought stocks"

@app.route("/sell/<userID>/<int:amount>")
def sellStocks(userID, amount):    
    holdings = getUserHoldingsDb(userID)['stock_amnt']
    if amount > holdings:
        return "Sorry you do not own enough stocks to sell that amount."
    # bank buys stock from user
    obsUpdateStockHoldings(amount,"buy")
    # user sells stock to bank
    updateUserHoldingsDb(userID, amount, "sell")
    return "sold stocks"

if __name__ == "__main__":
    app.run(debug=True)
#
