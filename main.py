"""
Will most likely want to store each user's information in a local database which will also store all admin stuff
Also get a second database to log all transactions for the admin interface.
"""


from flask import Flask, jsonify, request
import time, datetime
import mysql.connector
import requests
import string


adminToken = 'adminToken1337'
db_ip = '35.237.90.218'
db_username = 'stockUser'
db_password = '4ll_ur_st0ck_b3l0ng_t0_u5'
db_name = 'stockMicroservice'


#Each microservice can be pretty much a bank asset; probably need to store current bank status in a db
#Otherwise... where does user validation take place?

def error(msg):
	return jsonify({"error": msg})


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


#====================================================================


def query_db(db, query, params, fetch = False):
	#Use a cursor.
	cursor = db.cursor()
	if params:
		cursor.execute(query, params)
	else:
		cursor.execute(query)
	if not fetch:
		db.commit()
	if fetch:
		result = cursor.fetchall()
		cursor.close()
		return result
	cursor.close()
	return None

#Either connect to the users database or the log database...?
def establish_connection_with_db():
	try:
		db = mysql.connector.connect(host = db_ip,
							 user = db_username,
							 password = db_password,
							 database = db_name,
							 auth_plugin="mysql_native_password"
		)
		return db
	except:
		return -1

	
def getLogs():
	db = establish_connection_with_db()
	query = 'SELECT * FROM logs WHERE token = "adminToken1337"'
	res = query_db(db, query, None, True)
	return res
#====================================================================

#Make sure the token is pre-validated before doing this part.
def getUserStocks(token):
	db = establish_connection_with_db()
	query = "SELECT * FROM users WHERE token = (%s)" 
	res = query_db(db, query, (token,), True)
	amount = res[0][1]
	db.close()
	return amount


def getUserBalance(token):
	db = establish_connection_with_db()
	query = "SELECT * FROM users where token = (%s)"
	res = query_db(db, query, (token,), True)
	balance = res[0][2]
	db.close()
	return float(balance)


def validateToken(token):
	#Ideally we would query our userdb to see if such a user actually exists.
	db = establish_connection_with_db()
	query = "SELECT * FROM users WHERE token = (%s)"
	res = query_db(db, query, (token,), True)
	return len(res) > 0


#Update the current amount in the database here
def updateUserStocks(token, amount):
	price = float(getPrice())
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	#First log this transaction.
	db = establish_connection_with_db()
	query = "INSERT INTO logs(token, action, amount, time) VALUES (%s, %s, %s, %s)"
	#This is a sell
	if amount < 0:
		query_db(db, query, (token, "sell", abs(amount), timestamp))
	else:#Buy
		query_db(db, query, (token, "buy", abs(amount), timestamp))
	
	currentStocks = getUserStocks(token)
	currentBalance = getUserBalance(token)
	total = round(price * amount, 2)
	newStocks = currentStocks + amount
	newBalance = currentBalance - total
	
	#Then we want to update the amounts.
	query = "UPDATE users SET stocks = %s, balance = %s where token = %s"
	query_db(db, query, (newStocks, newBalance, token))
	
	return True


#Make a new user with 0 stocks and 0 profit.
def createUser(token):#pragma: no cover
	db = establish_connection_with_db()
	query = "INSERT INTO users(token, stocks, balance) VALUE (%s, %s, %s)"
	query_db(db, query, (token, 0, 0.0))
	return


def createApp():
	foo = Flask(__name__)

	#userID, amount 
	@foo.route('/buy', methods= ['POST'])
	def buy():
		json = request.get_json()
		if not json or 'userID' not in json or 'amount' not in json:
			return error("Invalid parameters.")
		token = json['userID']
		amount = int(json['amount'])#subject to change
		if not token or not amount:
			return error("Insufficient parameters. Please provide a valid user token and an amount to sell.")
	
		if not validateToken(token):
			return error("Invalid token")
		if not str(amount).isnumeric():#isnumeric prevents all floats and negative numbers, so we're pretty safe.
			return error("Invalid amount")
		
		#Currently no validation to see if the use has the money necessary to carry out this transaction
		
		#Here we will check if the bank has enough stocks, although it won't ever fail.
		amount = int(amount)
		currentAmount = int(getUserStocks('adminToken1337'))
		#If the bank doesn't have enough stocks, buy as many as is needed.
		if currentAmount < amount:
			updateUserStocks('adminToken1337', amount - currentAmount + 1)# +1 because the bank must at least have 1 stock.
		updateUserStocks('adminToken1337', -amount)
		updateUserStocks(token, amount)#Purchase x stocks
		
		current_user_shares = getUserStocks(token)
		current_bank_shares = getUserStocks('adminToken1337')
		result = {
			"obs_shares" : current_bank_shares,
			"user_shares" : current_user_shares
		}
		return jsonify(result)

	@foo.route('/sell', methods = ['POST'])
	def sell():
		json = request.get_json()
		if not json or 'userID' not in json or 'amount' not in json:
			return error("Invalid parameters.")
		token = json['userID']
		amount = json['amount']#subject to change
		if not token or not amount:
			return error("Insufficient parameters. Please provide a valid user token and an amount to sell.")
	
		if not validateToken(token):
			return error("Invalid token")
		if not str(amount).isnumeric():#isnumeric prevents all floats and negative numbers, so we're pretty safe.
			return error("Invalid amount")
		
		#Currently no validation to see if the user has the money necessary to carry out this transaction
		#Ideally we would do this here... but it's kinda weird
		
		#Here we will check if the token user has enough stocks to sell.
		amount = int(amount)
		if getUserStocks(token) < amount:
			return error("Cannot sell more stocks than are owned")
		
		#The user can sell this much, thus we want to update the total amount here.
		updateUserStocks(token, -amount)
		updateUserStocks('adminToken1337', amount)
		
		current_user_shares = getUserStocks(token)
		current_bank_shares = getUserStocks('adminToken1337')
		result = {
			"obs_shares" : current_bank_shares,
			"user_shares" : current_user_shares
		}
		return jsonify(result)
	

	#Require validation of token, thus restrict to only POST
	#I guess we're allowing anyone to get this then
	@foo.route('/getStockPrice', methods = ['GET'])
	def currentPrice():
		'''
		json = request.get_json()
		if not json or 'token' not in json:
			return error("No token provided")
	
		token = json['token']
		if not validateToken(token):
			return error("Invalid token provided")
		'''
		price = getPrice()
		response = {'price': price}
		return jsonify(response)
	
	@foo.route('/')
	def default():
		return "Greetings, nothing to see here..."
	
	
	#My version has to be a post request, for whatever reason...
	@foo.route('/getUserHoldings', methods = ['POST'])
	def getUserHoldings():
		json = request.get_json()
		if not json or 'userID' not in json:
			return error("No token provided")
		token = json['userID']
		if not validateToken(token):
			return error("Invalid token")
		return jsonify({'shares': getUserStocks(token)})
	
	#Call this endpoint to add a user.
	@foo.route('/addUser', methods = ['GET', 'POST'])
	def addUser():#pragma: no cover
		json = request.get_json()
		if not json or 'userID' not in json:
			return error("No token provided")
		token = json['userID']
		if validateToken(token):
			return error("User already exists")
		createUser(token)
		return jsonify({"status": "success"})
	
	#Will get the bank's current holdings.
	@foo.route('/getOBSHoldings', methods = ['GET'])
	def getBankStocks():
		return jsonify({'shares': getUserStocks('adminToken1337')})
	
	@foo.route('/getOBSLogs')
	def adminLogs():#pragma: no cover
		#Connect to database, only get things that have token = admin and get a list of all of the transaction logs
		logs = getLogs()
		print(logs)
		return "Admin logs..."
	
	return foo

#Need to create the 'app' this way so google app engine doesn't flip out
app = createApp()
if __name__ == '__main__':#pragma: no cover
	app.run(host = "127.0.0.1", port=8080, debug=False)
	
	
#Curl querying curl -d '{"userID": "sampleUser", "amount": 10}' -H "Content-Type: application/json" http://localhost:8080/buy

#curl -d '{"token": "sampleUser"}' -H "Content-Type: application/json" -X POST http://localhost:8080/addUser

#When deployed: curl -d '{"token": "foo"}' -H "Content-Type: application/json" -X POST http://sonorous-bounty-258117.appspot.com/getStockPrice

#curl -X GET -H "Content-Type: application/json" -d '{"userID": "sampleUser"}' http://sonorous-bounty-258117.appspot.com/getUserHoldings