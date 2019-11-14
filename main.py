"""
Will most likely want to store each user's information in a local database which will also store all admin stuff
Also get a second database to log all transactions for the admin interface.
"""
from flask import Flask, jsonify, request
import requests

#Each microservice can be pretty much a bank asset; probably need to store current bank status in a db
#Otherwise... where does user validation take place?

def validateToken(token):
	#Ideally we would query our userdb to see if such a user actually exists, alternatively we could query the central db.
	if not token:
		return False
	return True

def getPrice():
	headers = {"Accept":"application/json",
           "Authorization":"Bearer C8JeJKW7czXRFB04ze8acr8WORGn"}
	try:
		response = requests.get('https://sandbox.tradier.com/v1/markets/quotes?symbols=rtn', headers=headers)
		content = str(response.content)
		price = content.split('"last":')[1].split(',')[0]#Dumb parsing
		return price
	except:
		return "Error encountered when getting information"


#Will need to implement this properly; connects to database and sees how many stocks this user has.
def getUserStocks(token):
	return 1000

#Update the current amount in the database here
def updateUserStocks(token, amount):
	price = float(getPrice())
	#change by amount * price, log somewhere as well
	return True

def createApp():
	app = Flask(__name__)

	@app.route('/buy', methods= ['POST'])
	def buy():
		json = request.get_json()
		token = json['token']
		amount = json['amount']#subject to change
		if not token or not amount:
			response = {"error": "Insufficient parameters. Please provide a valid user token and an amount to sell."}
			return jsonify(response)
	
		if not validateToken(token):
			response = {"error": "Invalid token"}
			return jsonify(response)
		if not amount.isnumeric():#isnumeric prevents all floats and negative numbers, so we're pretty safe.
			response = {"error": "Invalid amount"}
			return jsonify(response)
		
		#Currently no validation to see if the use has the money necessary to carry out this transaction
		
		#Here we will check if the bank has enough stocks, although it won't ever fail.
		amount = int(amount)
		currentAmount = getUserStocks('admin')
		#If the bank doesn't have enough stocks, buy as many as is needed.
		if currentAmount < amount:
			updateUserStocks('admin', amount - currentAmount + 1)# +1 because the bank must at least have 1 stock.
		updateUserStocks('admin', -amount)
		updateUserStocks(token, amount)#Purchase x stocks
		
		return jsonify({"status:", "success"})

	@app.route('/sell', methods = ['POST'])
	def sell():
		json = request.get_json()
		token = json['token']
		amount = json['amount']#subject to change
		if not token or not amount:
			response = {"error": "Insufficient parameters. Please provide a valid user token and an amount to sell."}
			return jsonify(response)
	
		if not validateToken(token):
			response = {"error": "Invalid token"}
			return jsonify(response)
		if not amount.isnumeric():#isnumeric prevents all floats and negative numbers, so we're pretty safe.
			response = {"error": "Invalid amount"}
			return jsonify(response)
		
		#Currently no validation to see if the user has the money necessary to carry out this transaction
		#Ideally we would do this here... but it's kinda weird
		
		#Here we will check if the token user has enough stocks to sell.
		amount = int(amount)
		if getUserStocks(token) < amount:
			response = {"error": "Invalid amount"}
			return jsonify(response)
		
		#The user can sell this much, thus we want to update the total amount here.
		updateUserStock(token, -amount)
		return jsonify({"status:", "success"})
	

	#Require validation of token, thus restrict to only POST
	@app.route('/getStockPrice', methods = ['GET', 'POST'])
	def currentPrice():
		json = request.get_json()
		if not json or 'token' not in json:
			error = "No token provided"
			return jsonify({'error': error})
	
		token = json['token']
		if not validateToken(token):
			error = "Invalid token provided"
			return jsonify({'error': error})
		price = getPrice()
		response = {'price': price}
		return jsonify(response)
	
	
	@app.route('/getAdminLogs')
	def adminLogs():
		#Connect to database, only get things that have token = admin and get a list of all of the transaction logs
		return "Admin logs..."
	
	return app


if __name__ == "__main__":
	app = createApp()
	app.run(host = '127.0.0.1', port=8080)
	
	
#Curl querying curl -d '{"token": "foo"}' -H "Content-Type: application/json" -X POST http://localhost:8080/getStockPrice

