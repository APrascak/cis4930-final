 #!/usr/bin/env python3
# -*- coding: utf-8 -*-


from google.cloud import firestore
import requests
from flask import Flask
import datetime

db = firestore.Client.from_service_account_json('/Users/Sydney/Desktop/cis4930-final/PINSService/src/pinterestservice-firebase-adminsdk-6ubsp-9e03db19db.json')
app = Flask(__name__)


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

def getUserHoldingsDb(userID):
    doc_ref = db.collection(u'UserHoldings_PINS').document(userID)
 
    doc = doc_ref.get() 
    
    if doc.exists:
        return  doc.to_dict() 
    else:
        return {"shares" : 0}
  


def updateUserHoldingsDb(userID, amnt, action):

    currStocks = getUserHoldingsDb(userID)['shares']
    if action == "buy":
        updatedStocks = currStocks + amnt
    else:
        updatedStocks = currStocks - amnt
 
    doc_ref = db.collection(u'UserHoldings_PINS').document(userID)
    doc_ref = doc_ref.set({
            u'shares': updatedStocks
            })
    return 1

def obsGetAvailableStocks():
    doc_ref = db.collection(u'OBS_holdings').document('FGABKyqIk71Fn8e1n94j')
    doc = doc_ref.get() 
    if doc.exists:
        return  doc.to_dict() 
    else:
        return {"shares" : 0}
   
def obsUpdateStockHoldings(amount, action):
    # add or sell additional stocks
    currStocks = obsGetAvailableStocks()['shares']
    print("current ",currStocks)
    if action == "buy":
        updatedStocks = currStocks + amount
    else:
        updatedStocks = currStocks - amount            
    
    doc_ref = db.collection(u'OBS_holdings').document('FGABKyqIk71Fn8e1n94j')
    doc_ref = doc_ref.set({
            u'shares': updatedStocks,
            })
            
    return 1

def log_action(userID,amount,action):
	data = {
		"action": action,
		"user": userID,
		"amount": amount
	}
	print(data)
	print(data['action'])
	db.collection('logs').document(str(datetime.datetime.now())).set(data)


@app.route("/",) 
def index():
    return "Welcome to OBS Pinterest Service"

@app.route("/getStockPrice",)
def getStockPrice():
    result = {"stock_price": getPriceFromTradier()}
    return result

@app.route("/getUserHoldings/<userID>",) 
def getUser(userID):
    result =  getUserHoldingsDb(userID)
    return result

@app.route("/getOBSHoldings",) 
def getOBS():
    result =  obsGetAvailableStocks()
    return result 

@app.route("/buy/<userID>/<int:amount>")
def buyStocks(userID, amount):
    #check bank holdings
    bankholdings = obsGetAvailableStocks()['shares']
    action=u"buy"
    if amount > bankholdings:
        amntNeeded = amount - bankholdings 
        obsUpdateStockHoldings((amntNeeded + 5000), "buy")
    # bank sells stocks
    obsUpdateStockHoldings(amount, "sell")
    # user buys stock
    updateUserHoldingsDb(userID, amount, "buy")
    log_action(userID,amount,action)
    
    return { "obs_shares": obsGetAvailableStocks()['shares'], "user_shares": getUserHoldingsDb(userID)['shares'] }

@app.route("/sell/<userID>/<int:amount>")
def sellStocks(userID, amount):    
    holdings = getUserHoldingsDb(userID)['shares']
    action=u"sell"
    if amount > holdings:
        return "Sorry you do not own enough stocks to sell that amount."
    # bank buys stock from user
    obsUpdateStockHoldings(amount,"buy")
    # user sells stock to bank
    updateUserHoldingsDb(userID, amount, "sell")
    log_action(userID,amount,action)
    return { "obs_shares": obsGetAvailableStocks()['shares'], "user_shares": getUserHoldingsDb(userID)['shares'] }

if __name__ == "__main__":
    app.run(debug=True)
#
