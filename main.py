# Microservice for UBER
# Alex Prascak

from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route("/",)
def index():
	return "Python server"

def uber_price():
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

@app.route("/price",)
def price():
	return {"uber_price": uber_price()}

if __name__ == '__main__':
	app.run(debug=True)
