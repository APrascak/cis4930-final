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


def userFunds(token, timeStamp, balanceChange):
    data_to_upload = {
        'Token': token,
        'Time Stamp': timeStamp,
        'balance Change': balanceChange
    }
    DBConn.post('/CentralLogging/UserFunds/', data_to_upload)


def getUserHoldingsDb(userID):
    userDictionary = DBConn.get('/Central/Users/', '')
    for entry in userDictionary:
        result = DBConn.get('/Central/Users/'+entry+'/Stocks', '')
        if(DBConn.get('/Central/Users/'+entry+'/Token', '') == userID):
            return result
    return "User does not exist"


def obsGetAvailableStocks():
    bankDictionary = DBConn.get('/Central/Bank/', '')
    for entry in bankDictionary:
        return (DBConn.get('/Central/Bank/'+entry+'/Stock', ''))


@app.route('/',)
def home():
    return "Snapchat Microservice"


@app.route("/getStockPrice",)
def getStockPrice():
    result = {"stock_price ": getPriceFromTradier()}
    return result


@app.route("/getUserHoldings/<int:userID>",)
def getUser(userID):
    result = {"stock_amnt ": getUserHoldingsDb(userID)}
    return result


@app.route("/getOBSHoldings",)
def getOBS():
    result = "{obs_holdings: "+str(obsGetAvailableStocks())+"}"
    return result


@app.route('/buyStock/<int:token>/<int:amount>',)
def buyStock(token, amount):
    # replace with api call
    getStockPrice = getPriceFromTradier()
    totalPrice = amount * getStockPrice
    userDictionary = DBConn.get('/Central/Users/', '')
    # Updating Cental User Database - Users
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
    # Updating Central Database - Bank
    bankDictionary = DBConn.get('/Central/Bank/', '')
    for entry in bankDictionary:
        currentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
        newAmount = currentAmount - amount
        DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
    # Updating Central Logging Database - User Funds
    userFunds(token, current_time, totalPrice)
    return(str(result))


@app.route('/sellStock/<int:token>/<int:amount>',)
def sellStock(token, amount):
    # replace with api call
    getStockPrice = getPriceFromTradier()
    totalPrice = amount * getStockPrice
    userDictionary = DBConn.get('/Central/Users/', '')
    # Updating Cental User Database - Users
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
    # Updating Central Database - Bank
    bankDictionary = DBConn.get('/Central/Bank/', '')
    for entry in bankDictionary:
        currentAmount = DBConn.get('/Central/Bank/'+entry+'/Stock', '')
        newAmount = currentAmount + amount
        DBConn.put('/Central/Bank/'+entry, 'Stock', newAmount)
    # Updating Central Logging Database - User Funds
    userFunds(token, current_time, -totalPrice)
    return(str(result))


if(__name__) == "__main__":
    app.run(debug=True)
