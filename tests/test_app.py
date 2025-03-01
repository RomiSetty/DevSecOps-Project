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
    # First, add a goal so it exists in the tracker
    data = {
        "title": "Goal 1",
        "description": "Description for Goal 1"
    }
    response = client.post('/goals', json=data)

    # Ensure the goal was created successfully
    assert response.status_code == 201
    goal_data = response.get_json()
    
    # Now test retrieving the goal details by its ID (goal_id = 0)
    response = client.get(f'/goals/{goal_data["id"]}')  # Use the ID from the created goal

    # Assert the response status code is 200
    assert response.status_code == 200

    # Assert the response contains the goal's details
    response_json = response.get_json()
    assert response_json["title"] == "Goal 1"
    assert response_json["description"] == "Description for Goal 1"
    assert response_json["completed"] == False
