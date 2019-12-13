import requests
import json
from flask import Flask
from firebase import firebase
from flask_cors import CORS

app = Flask(__name__)
DBConn = firebase.FirebaseApplication('https://firestore-demo-3ebe9.firebaseio.com/', None)
CORS(app, resources={r"/*": {"origins": "*"}})

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


def getUserHoldingsDb(userID):
    userDictionary = DBConn.get('/Central/Users/', '')
    for entry in userDictionary:
        result = DBConn.get('/Central/Users/'+entry+'/Stocks', '')
        if(DBConn.get('/Central/Users/'+entry+'/Token', '') == userID):
            return result
    return 0;


def obsGetAvailableStocks():
    bankDictionary = DBConn.get('/Central/Bank/', '')
    for entry in bankDictionary:
        return (DBConn.get('/Central/Bank/'+entry+'/Stock', ''))


@app.route('/',)
def home():
    return "Snapchat Microservice"


@app.route("/getStockPrice",)
def getStockPrice():
    result = {"stock_price": getPriceFromTradier()}
    return result


@app.route("/getUserHoldings/<string:userID>",)
def getUser(userID):
    result = {"shares": getUserHoldingsDb(userID)}
    return result


@app.route("/getOBSHoldings",)
def getOBS():
    result = "{obs_holdings: "+str(obsGetAvailableStocks())+"}"
    return result


@app.route('/buy/<string:token>/<int:amount>',)
def buyStock(token, amount):
    userDictionary = DBConn.get('/Central/Users/', '')
    tell = 0
    userCurrentAmount = 0
    bankCurrentAmount = 0
    # Updating Cental User Database - Users
    for entry in userDictionary:
        if(DBConn.get('/Central/Users/'+entry+'/Token', '') == token):
            userCurrentAmount = DBConn.get('/Central/Users/'+entry+'/Stocks', '')
            newAmount = userCurrentAmount + amount
            userCurrentAmount = newAmount
            DBConn.put('/Central/Users/'+entry, 'Stocks', newAmount)
            tell = 1
            break
    if(tell == 0):
        data_to_upload = {
        'Token': token,
        'Stocks': amount
        }
        test = DBConn.post('/Central/Users/', data_to_upload)
        userCurrentAmount = DBConn.get('/Central/Users/'+test['name']+'/Stocks', '')
        bankDictionary = DBConn.get('/Central/Bank/', '')
        for entry in bankDictionary:
            bankCurrentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
            newAmount = bankCurrentAmount - amount
            bankCurrentAmount = newAmount
            DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
        return {"obs_shares": bankCurrentAmount, "user_shares": userCurrentAmount}
    # Updating Central Database - Bank
    bankDictionary = DBConn.get('/Central/Bank/', '')
    for entry in bankDictionary:
        bankCurrentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
        newAmount = bankCurrentAmount - amount
        bankCurrentAmount = newAmount
        DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
    return {"obs_shares": bankCurrentAmount, "user_shares": userCurrentAmount}


@app.route('/sell/<string:token>/<int:amount>',)
def sellStock(token, amount):
    userDictionary = DBConn.get('/Central/Users/', '')
    userCurrentAmount = 0
    bankCurrentAmount = 0
    # Updating Cental User Database - Users
    for entry in userDictionary:
        if(DBConn.get('/Central/Users/'+entry+'/Token', '') == token):
            userCurrentAmount = DBConn.get('/Central/Users/'+entry+'/Stocks', '')
            newAmount = userCurrentAmount - amount
            if (newAmount < 0):
                return "insufficient stocks"
            userCurrentAmount = newAmount
            DBConn.put('/Central/Users/'+entry, 'Stocks', newAmount)
            result = DBConn.get('/Central/Users/'+entry, '')
            break
    # Updating Central Database - Bank
    bankDictionary = DBConn.get('/Central/Bank/', '')
    for entry in bankDictionary:
        bankCurrentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
        newAmount = bankCurrentAmount + amount
        bankCurrentAmount = newAmount
        DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
    return {"obs_shares": bankCurrentAmount, "user_shares": userCurrentAmount}


if(__name__) == "__main__":
    app.run(debug=True)
