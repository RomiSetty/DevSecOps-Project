import pytest
from restapi import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to the Goal Tracking API!"

def test_list_goals(client):
    response = client.get('/goals')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_add_goal(client):
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    response = client.post('/goals', data=json.dumps(new_goal), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Learn Flask"
    assert data["description"] == "Complete the Flask course this month"
    assert data["completed"] == False

def test_show_goal_details(client):
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    response = client.post('/goals', data=json.dumps(new_goal), content_type='application/json')
    goal_id = json.loads(response.data)["id"]
    response = client.get(f'/goals/{goal_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["title"] == "Learn Flask"
    assert data["description"] == "Complete the Flask course this month"

def test_mark_goal_completed(client):
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    response = client.post('/goals', data=json.dumps(new_goal), content_type='application/json')
    goal_id = json.loads(response.data)["id"]
    response = client.put(f'/goals/{goal_id}', content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["completed"] == True

def test_delete_goal(client):
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    response = client.post('/goals', data=json.dumps(new_goal), content_type='application/json')
    goal_id = json.loads(response.data)["id"]
    response = client.delete(f'/goals/{goal_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == f"Goal 'Learn Flask' deleted"
    response = client.get(f'/goals/{goal_id}')
    assert response.status_code == 404
    assert "Invalid goal ID" in str(response.data)
