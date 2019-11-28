import pytest
from main import app
import requests
import json
from unittest.mock import patch
from main import getPriceFromTradier, obsGetAvailableStocks


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
                                params={'symbols': 'SNAP,VXX190517P00016000', 'greeks': 'false'},
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
    assert b"Snapchat Microservice" in response.data


def test_get_stock_price(test_client):
    """
    GIVEN a Flask application
    WHEN the '/getStockPrice' page is requested (GET)
    THEN check the response is current stock price from tradier
    """
    expectedPrice = getStockPrice()
    response = test_client.get('/getStockPrice')

    assert response.status_code == 200
    assert expectedPrice == json.loads(response.data)['stock_price ']


def test_get_stock_price_helper(test_client):
    assert getStockPrice() == getPriceFromTradier()


@patch('main.obsGetAvailableStocks')
def test_get_obs_holdings(mock_obsGetAvailableStocks, test_client):

    mock_obsGetAvailableStocks.return_value = {"shares": 5000}
    response = test_client.get('/getOBSHoldings')
    assert response.status_code == 200


@patch('main.getUserHoldingsDb')
def test_get_user_holdings(mock_getUserHoldingsDb, test_client):

    mock_getUserHoldingsDb.return_value = 10
    response = test_client.get('/getUserHoldings/234567')
    assert response.status_code == 200
    assert (json.loads(response.data)["stock_amnt "]) == 10

#
@patch('main.buyStock')
def test_user_buy_stock(mock_buyStock, test_client):
    mock_buyStock.return_value = 0
    response = test_client.get('/buyStock/234567/10')
    assert response.status_code == 200


@patch('main.sellStock')
def test_user_sell_Stock(mock_sellStock, test_client):
    mock_sellStock.return_value = 0
    response = test_client.get('/sellStock/234567/100')
    assert response.status_code == 200
