import json
import pytest
from flask import Flask
from flask.testing import FlaskClient

@pytest.fixture
def client() -> FlaskClient:
    app = Flask(__name__)

    # Define a simple route for testing
    @app.route('/goals')
    def list_goals():
        return "<ul><li>Goal 1</li><li>Goal 2</li></ul>", 200

    # Create the test client
    with app.test_client() as client:
        yield client

def test_list_goals(client):
    response = client.get('/goals')

    # Assert the response status code is 200
    assert response.status_code == 200

    # Assert the content type is HTML
    assert 'text/html' in response.content_type

    # Assert that the response contains a <ul> element (you can modify this based on the actual response)
    assert "<ul>" in response.data.decode('utf-8')
    assert "<li>Goal 1</li>" in response.data.decode('utf-8')
    assert "<li>Goal 2</li>" in response.data.decode('utf-8')

def test_show_goal_details(client):
    # You can modify this test similarly if you have another route that returns HTML content
    response = client.get('/goal/1')  # Assuming you have a /goal/<id> route

    # Check if the response is HTML
    assert 'text/html' in response.content_type
    assert response.status_code == 200

    # Modify to check for specific content based on the response
    assert "<h1>Goal 1 Details</h1>" in response.data.decode('utf-8')
