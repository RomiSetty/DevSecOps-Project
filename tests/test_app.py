import json
import pytest
from flask import Flask, request, jsonify
from flask.testing import FlaskClient

# Mock tracker
class Tracker:
    def __init__(self):
        self.goals = []
        self.id_counter = 1

    def add_goal(self, title, description):
        goal = {
            "id": self.id_counter,
            "title": title,
            "description": description,
            "completed": False
        }
        self.goals.append(goal)
        self.id_counter += 1
        return goal

    def get_goal(self, goal_id):
        for goal in self.goals:
            if goal["id"] == goal_id:
                return goal
        return None

# Initialize the tracker instance
tracker = Tracker()

@pytest.fixture
def client() -> FlaskClient:
    app = Flask(__name__)

    # Define routes for testing
    @app.route('/goals', methods=['GET'])
    def list_goals():
        return "<ul><li>Goal 1</li><li>Goal 2</li></ul>", 200

    @app.route('/goals', methods=['POST'])
    def add_goal():
        data = request.json
        if "title" not in data or "description" not in data:
            return jsonify({"error": "Title and description required"}), 400
        goal = tracker.add_goal(data["title"], data["description"])
        return jsonify(goal), 201

    @app.route('/goals/<int:goal_id>', methods=['GET'])
    def show_goal_details(goal_id):
        goal = tracker.get_goal(goal_id)
        if goal:
            return jsonify(goal)
        return jsonify({"error": "Goal not found"}), 404

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
    
    # Now test retrieving the goal details by its ID (goal_id = 1 in this case)
    response = client.get(f'/goals/{goal_data["id"]}')  # Use the ID from the created goal

    # Assert the response status code is 200
    assert response.status_code == 200

    # Assert the response contains the goal's details
    response_json = response.get_json()
    assert response_json["title"] == "Goal 1"
    assert response_json["description"] == "Description for Goal 1"
    assert response_json["completed"] == False
