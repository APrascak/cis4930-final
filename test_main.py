# tests for Pinterest Stock Service
# to run tests use terminal, cd into test directory, use command 'py.test'
# import pytest
# from main import app
# import requests
# import json
# from unittest.mock import Mock
# from unittest.mock import patch
# from main import get_price, update_obs_holdings, updates_user_holdings

import pytest
from main import app
import requests
import json
import mock
from mock import patch
from main import get_price, update_obs_holdings, updates_user_holdings


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
                                params={'symbols': 'AXP,VXX190517P00016000', 'greeks': 'false'},
                                headers={'Authorization': 'Bearer uZOWMJ0Hh2jcz2g9GE2Xa9YNPhMC', 'Accept': 'application/json'})
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
    assert b"OBS - American Express Microservice" in response.data
    
    
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

def test_get_stock_price_helper(test_client):
    assert getStockPrice() == get_price()
     
@patch('main.obs_holdings')
def test_get_obs_holdings(mock_obsGetAvailableStocks, test_client):
   
    mock_obsGetAvailableStocks.return_value = { "shares": 5000 }
    response = test_client.get('/getOBSHoldings')
    assert response.status_code == 200
    assert (json.loads(response.data)['obs_shares']) == 5000
    

@patch('main.user_holdings')
def test_get_user_holdings(mock_user_holdings, test_client):

    mock_user_holdings.return_value = { "shares": 10 }
    response = test_client.get('/getUserHoldings/test')    
    assert response.status_code == 200
    assert (json.loads(response.data)["user_shares"]) == 10

@patch('main.update_obs_holdings')
def test_update_obs_holdings(mock_update_obs_holdings, test_client):
    mock_update_obs_holdings.return_value = 0
    response = test_client.get('/buy/test/10')
    assert response.status_code == 200

@patch('main.update_obs_holdings')
@patch('main.updates_user_holdings') 
def test_user_buy_holdings(mock_update_obs_holdings, mock_updates_user_holdings, test_client):
    mock_update_obs_holdings.return_value = 0
    mock_updates_user_holdings.return_value = 0
    response = test_client.get('/buy/test/10')    
    assert response.status_code == 200

@patch('main.update_obs_holdings')
@patch('main.updates_user_holdings') 
def test_user_buy_holdings_a_lot_of_stocks(mock_update_obs_holdings, mock_updates_user_holdings, test_client):
    mock_update_obs_holdings.return_value = 0
    mock_updates_user_holdings.return_value = 0
    response = test_client.get('/buy/test/10000')    
    assert response.status_code == 200

@patch('main.update_obs_holdings')
@patch('main.updates_user_holdings') 
def test_user_sell_holdings(mock_update_obs_holdings, mock_updates_user_holdings, test_client):
    mock_update_obs_holdings.return_value = 0
    mock_updates_user_holdings.return_value = 0
    response = test_client.get('/sell/test/10')    
    assert response.status_code == 200
    
@patch('main.update_obs_holdings')
@patch('main.updates_user_holdings') 
def test_user_cannot_sell_more_than_holdings(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):
    test_holdings = test_client.get('/getUserHoldings/test') 
    prev_stocks = int(json.loads(test_holdings.data)['user_shares'])
    mock_obsUpdateStockHoldings.return_value = 0
    mock_updateUserHoldingsDb.return_value =0
    response = test_client.get('/sell/test/'+str(prev_stocks+100))    
    assert response.status_code == 200
    assert b"Error: insufficient user inventory." in response.data

    
@patch('main.update_obs_holdings')
@patch('main.updates_user_holdings') 
def test_user_sells_all_holdings(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):

    test_holdings = test_client.get('/getUserHoldings/test')  
    prev_stocks = int(json.loads(test_holdings.data)['user_shares'])
    
    mock_obsUpdateStockHoldings.return_value = 0
    mock_updateUserHoldingsDb.return_value =0
    response = test_client.get('/sell/test/'+str(prev_stocks))    
    assert response.status_code == 200
    assert b"Error: insufficient user inventory." not in response.data