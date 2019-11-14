# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:55:36 2019

@author: rudra
"""

"""SNAPCHAT"""
import centralLogging
import requests
from flask import Flask
from firebase import firebase
from datetime import datetime

app = Flask(__name__)
DBConn = firebase.FirebaseApplication('https://firestore-demo-3ebe9.firebaseio.com/', None)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def getPriceFromTradier():
    try:
        response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                                params={'symbols': 'SNAP,VXX190517P00016000', 'greeks': 'false'},
                                headers={'Authorization': 'Bearer uZOWMJ0Hh2jcz2g9GE2Xa9YNPhMC', 'Accept': 'application/json'})
    except requests.exceptions.RequestException as e:
        print("Get stock price request error: ", e)
        
    resp_json = response.json()
    lastPrice = resp_json["quotes"]["quote"]["last"]
    return lastPrice

@app.route('/',)
def home():
    return "visit: /buyStock or /sellStock"

@app.route('/buyStock',)
def buyStock(token, amount):
    #replace with api call
    getStockPrice = getPriceFromTradier()
    totalPrice = amount * getStockPrice
    userDictionary = DBConn.get('/Central/Users/','')
    #Updating Cental User Database - Users
    for entry in userDictionary:
        if(DBConn.get('/Central/Users/'+entry+'/Token', '') == token):
            balance = DBConn.get('/Central/Users/'+entry+'/Balance', '')
            currentAmount = DBConn.get('/Central/Users/'+entry+'/Stocks', '')
            newBalance = balance - totalPrice
            newAmount = currentAmount + amount
            DBConn.put('/Central/Users/'+entry, 'Balance', newBalance)
            DBConn.put('/Central/Users/'+entry, 'Stocks', newAmount)
            result = DBConn.get('/Central/Users/'+entry, '')
            break
    #Updating Central Database - Bank
    bankDictionary = DBConn.get('/Central/Bank/','')
    for entry in bankDictionary:
        currentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
        newAmount = currentAmount - amount
        DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
    #Updating Central Logging Database - User Funds
    centralLogging.userFunds(token, current_time, totalPrice)
    return(result)
    
@app.route('/sellStock',)
def sellStock(token, amount):
    #replace with api call
    getStockPrice = getPriceFromTradier()
    totalPrice = amount * getStockPrice
    userDictionary = DBConn.get('/Central/Users/','')
    #Updating Cental User Database - Users
    for entry in userDictionary:
        if(DBConn.get('/Central/Users/'+entry+'/Token', '') == token):
            balance = DBConn.get('/Central/Users/'+entry+'/Balance', '')
            currentAmount = DBConn.get('/Central/Users/'+entry+'/Stocks', '')
            newBalance = balance + totalPrice
            newAmount = currentAmount - amount
            DBConn.put('/Central/Users/'+entry, 'Balance', newBalance)
            DBConn.put('/Central/Users/'+entry, 'Stocks', newAmount)
            result = DBConn.get('/Central/Users/'+entry, '')
            break
    #Updating Central Database - Bank
    bankDictionary = DBConn.get('/Central/Bank/','')
    for entry in bankDictionary:
        currentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
        newAmount = currentAmount + amount
        DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
    #Updating Central Logging Database - User Funds
    centralLogging.userFunds(token, current_time, -totalPrice)
    return(result)
    
buyStock(123456, 1)

if(__name__) == "__main__":
    app.run(debug=True)