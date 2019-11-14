import pytest, json
from pytest_mock import mocker
from main import *


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
		"token": "yeet"
	}
	response = getStockPrice_client.get('/getStockPrice', json=data, content_type="application/json")
	assert response.status_code == 200


def test_getStockPrice_price(getStockPrice_client):
	data = {
		"token": "yeet"
	}
	response = getStockPrice_client.get('/getStockPrice', json=data, content_type="application/json")
	data = json.loads(response.data)
	assert data['price'] == 1337