# Microservice for UBER
# Alex Prascak

from flask import Flask
import httplib
import json

app = Flask(__name__)

@app.route("/",)
def index():
	return "Python server"

@app.route("/price",)
def price():
	# Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
	connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

	# Headers
	headers = {"Accept":"application/json",
	           "Authorization":"Bearer n7UzJWyS028Oi8PianpcNseKBI6j"}

	# Send synchronously
	connection.request('GET', '/v1/markets/quotes?symbols=uber', None, headers)
	try:
	  response = connection.getresponse()
	  content = response.read()
	  json_data = json.loads(content)
	  return json_data['quotes']['quote']['last'] # most recent price

	except httplib.HTTPException, e:
	  return('Exception during request')
