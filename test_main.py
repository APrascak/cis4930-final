# tests
# to run tests use terminal, cd into test directory, use command 'py.test'
import pytest
from main import app
import requests
import json
import mock
from mock import patch
from main import get_price, update_obs_holdings, update_user_holdings




@pytest.fixture(scope='module')
def test_client(): 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()
    
    # Establish an application context before running the tests.
    ctx = app.app_context()  
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
    ctx.pop()
    

def getStockPrice():
    try:
        response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
			params={'symbols': 'UBER,VXX190517P00016000', 'greeks': 'false'},
			headers={'Authorization': 'Bearer n7UzJWyS028Oi8PianpcNseKBI6j', 'Accept': 'application/json'}
		)
    except requests.exceptions.RequestException as e:
        print("Get stock price request error: ", e)
        
    resp_json = response.json()
    lastPrice = resp_json["quotes"]["quote"]["last"]
    return lastPrice


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"OBS Uber Microservice" in response.data

def test_home_page_patch(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"OBS Uber Microservice" in response.data
    
    
def test_get_stock_price(test_client):
    """
    GIVEN a Flask application
    WHEN the '/getStockPrice' page is requested (GET)
    THEN check the response is current stock price from tradier
    """
    expectedPrice = getStockPrice()
    response = test_client.get('/getStockPrice') 
    
    assert response.status_code == 200
    assert expectedPrice == json.loads( response.data )['stock_price']
     
@patch('main.obs_holdings')
def test_get_obs_holdings(mock_obsGetAvailableStocks, test_client):
    """
    GIVEN a Flask application
    WHEN the '/getStockPrices' page is requested (GET)
    THEN check the response is current stock price from tradier
    """
    mock_obsGetAvailableStocks.return_value = { "shares": 10 }
    response = test_client.get('/getOBSHoldings')    
    print(json.loads(response.data))
    assert response.status_code == 200
    assert (json.loads(response.data)['shares']) == 10

@patch('main.user_holdings')
def test_get_user_holdings(mock_getUserHoldingsDb, test_client):

    mock_getUserHoldingsDb.return_value = { "shares": 10 }
    response = test_client.get('/getUserHoldings/testing@uber.com')    
    assert response.status_code == 200
    assert (json.loads(response.data)["shares"]) == 10

def test_get_stock_price_helper(test_client):
    assert getStockPrice() == get_price()

@patch('main.update_obs_holdings')
@patch('main.update_user_holdings') 
def test_user_buy_stock(mock_update_obs_holdings, mock_update_user_holdings, test_client):
 
    mock_update_obs_holdings.return_value = 0
    mock_update_obs_holdings.return_value = 0
    response = test_client.get('/buy/testing@uber.com/100')    
    assert response.status_code == 200

@patch('main.update_obs_holdings')
@patch('main.update_user_holdings') 
def test_user_sell_holdings(mock_update_obs_holdings, mock_update_user_holdings, test_client):
    mock_update_obs_holdings.return_value = 0
    mock_update_user_holdings.return_value =0
    response = test_client.get('/sell/testing@uber.com/100')    
    assert response.status_code == 200

@patch('main.update_obs_holdings')
@patch('main.update_user_holdings') 
def test_user_cannot_sell_more_than_holdings(mock_update_obs_holdings, mock_update_user_holdings, test_client):
    test_holdings = test_client.get('/getUserHoldings/testing@uber.com') 
    prev_stocks = json.loads(test_holdings.data)['shares']
    mock_update_obs_holdings.return_value = 0
    mock_update_user_holdings.return_value =0
    response = test_client.get('/sell/testing@uber.com/'+str(prev_stocks+100))    
    assert response.status_code == 200
    assert b"Error: insufficient user inventory." in response.data

@patch('main.update_obs_holdings')
@patch('main.update_user_holdings') 
def test_user_sells_all_holdings(mock_update_obs_holdings, mock_update_user_holdings, test_client):

    test_holdings = test_client.get('/getUserHoldings/testing@uber.com')  
    prev_stocks = json.loads(test_holdings.data)['shares']
    
    mock_update_obs_holdings.return_value = 0
    mock_update_user_holdings.return_value =0
    response = test_client.get('/sell/testing@uber.com/'+str(prev_stocks))    
    assert response.status_code == 200
    assert b"Error: insufficient user inventory." not in response.data