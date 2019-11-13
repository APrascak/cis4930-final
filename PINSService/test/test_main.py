# tests for Pinterest Stock Service
# to run tests use terminal, cd into test directory, use command 'py.test'



import pytest
from src.main import app

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



def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Python Server" in response.data

