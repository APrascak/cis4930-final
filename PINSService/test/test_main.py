# tests for Pinterest Stock Service
# to run tests use terminal, cd into test directory, use command 'py.test'
import pytest
from src.main import app
import requests
import json
from unittest.mock import patch
from src.main import getPriceFromTradier, db, obsGetAvailableStocks



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
    assert b"Welcome to OBS Pinterest Service" in response.data
    
    
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
    assert getStockPrice() == getPriceFromTradier()
    

     
@patch('src.main.obsGetAvailableStocks')
def test_get_obs_holdings(mock_obsGetAvailableStocks, test_client):
   
    mock_obsGetAvailableStocks.return_value = { "shares": 5000 }
    response = test_client.get('/getOBSHoldings')    
    assert response.status_code == 200
    

@patch('src.main.getUserHoldingsDb')
def test_get_user_holdings(mock_getUserHoldingsDb, test_client):

    mock_getUserHoldingsDb.return_value = { "shares": 10 }
    response = test_client.get('/getUserHoldings/test')    
    assert response.status_code == 200
    assert (json.loads(response.data)["shares"]) == 10
 
@patch('src.main.obsUpdateStockHoldings')
def test_update_obs_holdings(mock_obsUpdateStockHoldings, test_client):
    mock_obsUpdateStockHoldings.return_value = 0
    response = test_client.get('/buy/test/10')
    assert response.status_code == 200
    
@patch('src.main.obsUpdateStockHoldings')
@patch('src.main.updateUserHoldingsDb') 
def test_user_buy_stock(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):
 
    mock_obsUpdateStockHoldings.return_value = 0
    mock_obsUpdateStockHoldings.return_value = 0
    response = test_client.get('/buy/test/100')    
    assert response.status_code == 200

@patch('src.main.obsUpdateStockHoldings')
@patch('src.main.updateUserHoldingsDb') 
def test_user_buy_holdings_a_lot_of_stocks(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):
    mock_obsUpdateStockHoldings.return_value = 0
    mock_updateUserHoldingsDb.return_value = 0
    response = test_client.get('/buy/test/10000')    
    assert response.status_code == 200
    
@patch('src.main.obsUpdateStockHoldings')
@patch('src.main.updateUserHoldingsDb') 
def test_user_sell_holdings(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):
    mock_obsUpdateStockHoldings.return_value = 0
    mock_updateUserHoldingsDb.return_value =0
    response = test_client.get('/sell/test/100')    
    assert response.status_code == 200
    
@patch('src.main.obsUpdateStockHoldings')
@patch('src.main.updateUserHoldingsDb') 
def test_user_cannot_sell_more_than_holdings(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):
    test_holdings = test_client.get('/getUserHoldings/test') 
    prev_stocks = json.loads(test_holdings.data)['shares']
    mock_obsUpdateStockHoldings.return_value = 0
    mock_updateUserHoldingsDb.return_value =0
    response = test_client.get('/sell/test/'+str(prev_stocks+100))    
    assert response.status_code == 200
    assert b"Sorry you do not own enough stocks to sell that amount." in response.data

    
@patch('src.main.obsUpdateStockHoldings')
@patch('src.main.updateUserHoldingsDb') 
def test_user_sells_all_holdings(mock_obsUpdateStockHoldings, mock_updateUserHoldingsDb, test_client):

    test_holdings = test_client.get('/getUserHoldings/test')  
    prev_stocks = json.loads(test_holdings.data)['shares']
    
    mock_obsUpdateStockHoldings.return_value = 0
    mock_updateUserHoldingsDb.return_value =0
    response = test_client.get('/sell/test/'+str(prev_stocks))    
    assert response.status_code == 200
    assert b"Sorry you do not own enough stocks to sell that amount." not in response.data
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    