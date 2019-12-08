# Microservice for UBER
# Alex Prascak

from flask import Flask
from google.cloud import firestore
from flask_cors import CORS
import requests
import json
import datetime


app = Flask(__name__)
db = firestore.Client.from_service_account_json('uber-stock-microservice-firebase-adminsdk-vzk11-6813665ba9.json')

CORS(app, resources={r"/*": {"origins": "*"}})

# Returns: current Uber stock price.
def get_price():
	try:
		response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
			params={'symbols': 'UBER,VXX190517P00016000', 'greeks': 'false'},
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
		return {"shares": (doc.to_dict()['shares'])}
	except:
		return 'Error.'

def obs_holdings():
	ref = db.collection('obs-holding').document("obs-uber")
	try:
		doc = ref.get()
		return {"shares": (doc.to_dict()['shares'])}
	except:
		return 'Error'

def update_obs_holdings(amount):
	ref = db.collection('obs-holding').document("obs-uber")
	try:
		ref.set({
			u"shares": amount
		})
	except:
		return False

def update_user_holdings(userID, amount):
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
	db.collection('logs').document(str(datetime.datetime.now())).set(data)

@app.route("/",)
def index():
	return "OBS Uber Microservice"

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
	obs_position = obs_holdings()['shares']
	action = u"buy"
	if amount >= obs_position:
		update_obs_holdings(5000)
		update_user_holdings(userID,amount)
		log_action(userID,amount,action)
	else:
		update_obs_holdings(obs_position - amount)
		update_user_holdings(userID,amount)
		log_action(userID,amount,action)
	return {
		"obs_shares": obs_holdings()['shares'],
		"user_shares": user_holdings(userID)['shares']
	}

@app.route("/sell/<userID>/<int:amount>")
def sell(userID, amount):
	obs_position = obs_holdings()['shares']
	user_position = user_holdings(userID)['shares']
	action=u"sell"
	if amount > user_position:
		return 'Error: insufficient user inventory.'
	else:
		# Add sale implementation
		update_obs_holdings(obs_position + amount)
		update_user_holdings(userID,amount * -1)
		log_action(userID,amount,action)
		return {
			"obs_shares": obs_holdings()['shares'],
			"user_shares": user_holdings(userID)['shares']
		}

if __name__ == '__main__':
	app.run(debug=True)