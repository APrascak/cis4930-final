
from flask import Flask
from google.cloud import firestore
import requests
import json
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
db = firestore.Client.from_service_account_json('cisproject2-firebase-adminsdk-p3dru-ffd0d7e5ed.json')

def get_price():
	try:
		response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
			params={'symbols': 'AXP,VXX190517P00016000', 'greeks': 'false'},
			headers={'Authorization': 'Bearer n7UzJWyS028Oi8PianpcNseKBI6j', 'Accept': 'application/json'}
		)
	except requests.exceptions.RequestException as e:
	  return('Exception during request' + str(e))
	else:
		json_response = response.json()
		price = json_response["quotes"]["quote"]["last"]
		return price

def user_holdings(userID):
	ref = db.collection('user-shares').document(userID)
	try:
		doc = ref.get()
		if doc.exists:
			return {"shares": (doc.to_dict()['shares'])}
		else:
			return {"shares" : 0}
	except:
		return 'Error.'

def obs_holdings():
	ref = db.collection('obs').document("axp")
	try:
		doc = ref.get()
		if doc.exists:
			return {"shares": (doc.to_dict()['shares'])}
		else:
			return {"shares" : 0}
	except:
		return 'Error'

def update_obs_holdings(amount):
	ref = db.collection('obs').document("axp")
	try:
		ref.set({
			u"shares": amount
		})
	except:
		return False

def updates_user_holdings(userID, amount):
	ref = db.collection('user-shares').document(userID)
	current_holdings = ref.get().to_dict()['shares']
	try:
		ref.set({
			u"shares": (current_holdings + amount)
		})
	except:
		print("Error occured during user stock purchasing.")

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
	return "OBS - American Express Microservice"

@app.route("/getStockPrice",)
def price():
	return {"stock_price": get_price()}

@app.route("/getUserHoldings/<userID>",)
def userHoldings(userID):
	return {"shares": user_holdings(userID)['shares']}

@app.route("/getOBSHoldings",)
def obsHoldings():
	return {"shares": obs_holdings()['shares']}

@app.route("/buy/<userID>/<int:amount>")
def buy(userID,amount):
	obs_position = int(obs_holdings()['shares'])
	action=u"buy"
	if amount >= obs_position:
		update_obs_holdings(5000)
	else:
		update_obs_holdings(obs_position - amount)
	updates_user_holdings(userID,amount)
	log_action(userID,amount,action)
	return {"testing": obs_holdings()['shares']}

@app.route("/sell/<userID>/<int:amount>")
def sell(userID, amount):
	obs_position = int(obs_holdings()['shares'])
	user_position = int(user_holdings(userID)['shares'])
	action=u"sell"
	if amount > user_position:
		return 'Error: insufficient user inventory.'
	else:
		log_action(userID,amount,action)
		return {
			"user": userID,
			"shares": amount
		}

if __name__ == '__main__':
	app.run(debug=True)