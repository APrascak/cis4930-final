"""
Will most likely want to store each user's information in a local database which will also store all admin stuff
Also get a second database to log all transactions for the admin interface.
"""
from flask import Flask, jsonify, request
import mysql.connector
import requests


adminToken = 'adminToken1337'
db_ip = '35.237.90.218'
db_username = 'stockUser'
db_password = '4ll_ur_st0ck_b3l0ng_t0_u5'
db_name = 'stockMicroservice'


#Each microservice can be pretty much a bank asset; probably need to store current bank status in a db
#Otherwise... where does user validation take place?

def error(msg):
	return jsonify({"error": msg})

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


#Insert into users with balance = 0
def createNewUser(token):
	return True

#Will need to implement this properly; connects to database and sees how many stocks this user has.
def getUserStocks(token):
	db = establish_connection_with_db()
	query = "SELECT * FROM users WHERE token = (%s)" 
	res = query_db(db, query, (token,), True)
	amount = res[0][1]
	db.close()
	return amount



def validateToken(token):
	#Ideally we would query our userdb to see if such a user actually exists.
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


#Update the current amount in the database here
def updateUserStocks(token, amount):
	price = float(getPrice())
	#change by amount * price, log somewhere as well
	return True


def createApp():
	foo = Flask(__name__)

	@foo.route('/buy', methods= ['POST'])
	def buy():
		json = request.get_json()
		token = json['token']
		amount = json['amount']#subject to change
		if not token or not amount:
			return error("Insufficient parameters. Please provide a valid user token and an amount to sell.")
	
		if not validateToken(token):
			return error("Invalid token")
		if not amount.isnumeric():#isnumeric prevents all floats and negative numbers, so we're pretty safe.
			return error("Invalid amount")
		
		#Currently no validation to see if the use has the money necessary to carry out this transaction
		
		#Here we will check if the bank has enough stocks, although it won't ever fail.
		amount = int(amount)
		currentAmount = getUserStocks('admi')
		#If the bank doesn't have enough stocks, buy as many as is needed.
		if currentAmount < amount:
			updateUserStocks('admin', amount - currentAmount + 1)# +1 because the bank must at least have 1 stock.
		updateUserStocks('admin', -amount)
		updateUserStocks(token, amount)#Purchase x stocks
		
		return jsonify({"status:", "success"})

	@foo.route('/sell', methods = ['POST'])
	def sell():
		json = request.get_json()
		token = json['token']
		amount = json['amount']#subject to change
		if not token or not amount:
			return error("Insufficient parameters. Please provide a valid user token and an amount to sell.")
	
		if not validateToken(token):
			return error("Invalid token")
		if not amount.isnumeric():#isnumeric prevents all floats and negative numbers, so we're pretty safe.
			return error("Invalid amount")
		
		#Currently no validation to see if the user has the money necessary to carry out this transaction
		#Ideally we would do this here... but it's kinda weird
		
		#Here we will check if the token user has enough stocks to sell.
		amount = int(amount)
		if getUserStocks(token) < amount:
			return error("Invalid amount")
		
		#The user can sell this much, thus we want to update the total amount here.
		updateUserStock(token, -amount)
		return jsonify({"status:", "success"})
	

	#Require validation of token, thus restrict to only POST
	@foo.route('/getStockPrice', methods = ['GET', 'POST'])
	def currentPrice():
		json = request.get_json()
		if not json or 'token' not in json:
			return error("No token provided")
	
		token = json['token']
		if not validateToken(token):
			return error("Invalid token provided")
		price = getPrice()
		response = {'price': price}
		return jsonify(response)
	
	@foo.route('/')
	def default():
		return "Hello there"
	
	@foo.route('/getUserStock', methods = ['GET', 'POST'])
	def getStocks():
		json = request.get_json()
		if not json or 'token' not in json:
			return error("No token provided")
		token = json['token']
		return jsonify({'amount': getUserStocks(token)})
		
	@foo.route('/getAdminLogs')
	def adminLogs():
		#Connect to database, only get things that have token = admin and get a list of all of the transaction logs
		return "Admin logs..."
	
	return foo

#Need to create the 'app' this way so google app engine doesn't flip out
app = createApp()
if __name__ == '__main__':
	app.run(host = "127.0.0.1", port=8080, debug=False)
	
	
#Curl querying curl -d '{"token": "adminToken1337"}' -H "Content-Type: application/json" -X POST http://localhost:8080/getStockPrice
#When deployed: curl -d '{"token": "foo"}' -H "Content-Type: application/json" -X POST http://sonorous-bounty-258117.appspot.com/getStockPrice
