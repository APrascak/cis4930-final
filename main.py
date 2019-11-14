# Microservice for UBER
# Alex Prascak

from flask import Flask
from google.cloud import firestore
import requests
import json

app = Flask(__name__)
db = firestore.Client.from_service_account_json('uber-stock-microservice-firebase-adminsdk-vzk11-6813665ba9.json')

# Returns: current Uber stock price.
def get_price():
	try:
		response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
			params={'symbols': 'UBER,VXX190517P00016000', 'greeks': 'false'},
			headers={'Authorization': 'Bearer n7UzJWyS028Oi8PianpcNseKBI6j', 'Accept': 'application/json'}
		)
	except requests.exceptions.RequestException as e:
	  return('Exception during request')
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

@app.route("/",)
def index():
	return "OBS Uber Microservice"

@app.route("/price",)
def price():
	return {"uber_price": get_price()}

@app.route("/userHoldings/<userID>",)
def userHoldings(userID):
	return {"user_shares": user_holdings(userID)['shares']}

@app.route("/obsHoldings",)
def obsHoldings():
	return {"obs_shares": obs_holdings()['shares']}

@app.route("/buy/<userID>/<int:amount>")
def buy(userID,amount):
	return "Stocks successfully purchased."

if __name__ == '__main__':
	app.run(debug=True)
