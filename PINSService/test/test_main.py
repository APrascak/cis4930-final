# tests for Pinterest Stock Service
# to run tests use terminal, cd into test directory, use command 'py.test'



import pytest
from src.main import app
import requests
import json
from unittest.mock import patch




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
                                params={'symbols': 'PINS,VXX190517P00016000', 'greeks': 'false'},
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
    assert b"Welcome to Python Server" in response.data

def test_home_page_patch(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Python Server" in response.data
    
    
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
     
@patch('src.main.obsGetAvailableStocks', return_value="10")
def test_get_obs_holdings(mock_obsGetAvailableStocks, test_client):
    """
    GIVEN a Flask application
    WHEN the '/getStockPrices' page is requested (GET)
    THEN check the response is current stock price from tradier
    """
    mock_obsGetAvailableStocks.return_value = { "total_stocks": 10, "cost_to_bank": 100 }
    response = test_client.get('/getOBSHoldings')    
    print(json.loads(response.data))
    assert response.status_code == 200
    assert (json.loads(response.data)['stock_amnt']) == 10
    
    
    
    
    
    
    