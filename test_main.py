import pytest, json
from pytest_mock import mocker
from main import *

def test_getPrice(mocker):
	response = mocker.Mock()
	response.content = '"last":1234,'
	mocker.patch('requests.get', return_value = response)
	val = getPrice()
	assert val == '1234'

def test_db(mocker):
	mocker.patch('mysql.connector.connect', return_value=True)
	assert establish_connection_with_db() == True




@pytest.fixture
def getStockPrice_client(mocker):
	#db = mocker.Mock()
	mocker.patch('main.getPrice', return_value = 1337)
	app = createApp()
	testing_client = app.test_client()
	ctx = app.app_context()
	ctx.push()
	
	yield testing_client
	ctx.pop()
	
	
#Check 
def test_getStockPrice_status(getStockPrice_client):
	data = {
		"userID": "yeet"
	}
	response = getStockPrice_client.get('/getStockPrice', json=data, content_type="application/json")
	assert response.status_code == 200

def test_getStockPrice_price(getStockPrice_client):
	response = getStockPrice_client.get('/getStockPrice', content_type="application/json")
	data = json.loads(response.data)
	assert data['price'] == 1337
	
	
@pytest.fixture
def getUserStocks_client(mocker):
	db = mocker.Mock()
	db.cursor.fetchall = mocker.Mock(return_value=[('testUser', 4242, 13.37)])
	db.cursor().fetchall = mocker.Mock(return_value=[('testUser', 4242, 13.37)])
	mocker.patch('main.establish_connection_with_db', return_value=db)
	mocker.patch('main.validateToken', return_value=True)
	app = createApp()
	testing_client = app.test_client()
	ctx = app.app_context()
	ctx.push()
	
	yield testing_client
	ctx.pop
	
def test_getUserStocks_func(getUserStocks_client):
	data = {
		"userID": "tylerTester"
	}
	response = getUserStocks_client.post('/getUserHoldings', json=data, content_type="application/json")
	assert response.status_code == 200
	data = json.loads(response.data)
	assert data['shares'] == 4242
	
def test_getOBSStocks_func(getUserStocks_client):
	response = getUserStocks_client.get('/getOBSHoldings')
	assert response.status_code == 200
	data = json.loads(response.data)
	assert data['shares'] == 4242
	
	
@pytest.fixture
def buy_client(mocker):
	mocker.patch("main.validateToken", return_value=True)
	mocker.patch('main.getUserStocks', return_value=1337)
	mocker.patch('main.updateUserStocks', return_value=None)
	app = createApp()
	testing_client = app.test_client()
	ctx = app.app_context()
	ctx.push()
	
	yield testing_client
	ctx.pop
	
def test_buy(buy_client):
	data = {
		"userID" : "moreTesting",
		"amount" : 20
	}
	response = buy_client.post('/buy', json=data, content_type="application/json")
	result = json.loads(response.data)
	assert result['obs_shares'] == 1337
	assert result['user_shares'] == 1337

	
@pytest.fixture
def sell_client(mocker):
	mocker.patch("main.validateToken", return_value=True)
	mocker.patch('main.getUserStocks', return_value=1337)
	mocker.patch('main.updateUserStocks', return_value=None)
	app = createApp()
	testing_client = app.test_client()
	ctx = app.app_context()
	ctx.push()
	
	yield testing_client
	ctx.pop
	
def test_sell(sell_client):
	data = {
		"userID" : "moreTesting",
		"amount" : 20
	}
	response = sell_client.post('/sell', json=data, content_type="application/json")
	result = json.loads(response.data)
	assert result['obs_shares'] == 1337
	assert result['user_shares'] == 1337
	
def test_bad_sell(sell_client):
	data = {
		"userID" : "moreTesting",
		"amount" : 2000
	}
	response = sell_client.post('/sell', json=data, content_type="application/json")
	result = json.loads(response.data)
	assert result['error'] == "Cannot sell more stocks than are owned"
	
def test_validate(getUserStocks_client):
	assert validateToken('testUser')


def test_getBalance(mocker):
	db = mocker.Mock()
	db.cursor.fetchall = mocker.Mock(return_value=[('testUser', 4242, 13.37)])
	db.cursor().fetchall = mocker.Mock(return_value=[('testUser', 4242, 13.37)])
	mocker.patch('main.establish_connection_with_db', return_value=db)
	balance = getUserBalance('testUser')
	assert balance == 13.37
	
def test_update_raw(mocker):
	mocker.patch('time.time', return_value = 1573792012)
	
	#Snip out the query part
	mocker.patch('main.establish_connection_with_db', return_value = 'fakedb')
	mocker.patch('main.query_db', return_value = 'norealquery')
	
	mocker.patch('main.getUserStocks', return_value = 100)
	mocker.patch('main.getPrice', return_value = 10)
	mocker.patch('main.getUserBalance', return_value = 100)
	assert updateUserStocks("testToken", 10)
	#getUserBalance.assert_any_call('testToken')
	#query_db.assert_any_call('fakedb', "UPDATE users SET stocks = %s, balance = %s where token = %s", (100 + 1000, 100 - 1000, "testToken"))