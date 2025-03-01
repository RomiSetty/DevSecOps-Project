from restapi import app
import json

# Test for Home Route
def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to the Goal Tracking API!"

# Test for GET /goals (List all goals)
def test_list_goals():
    response = app.test_client().get('/goals')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)  # Ensures the response is a list

# Test for POST /goals (Create a new goal)
def test_add_goal():
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    response = app.test_client().post('/goals', data=json.dumps(new_goal), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Learn Flask"
    assert data["description"] == "Complete the Flask course this month"
    assert data["completed"] == False  # New goal should not be completed

# Test for GET /goals/{id} (Get a specific goal)
def test_show_goal_details():
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    # Add goal first
    response = app.test_client().post('/goals', data=json.dumps(new_goal), content_type='application/json')
    goal_id = json.loads(response.data)["id"]

    # Fetch the specific goal
    response = app.test_client().get(f'/goals/{goal_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["title"] == "Learn Flask"
    assert data["description"] == "Complete the Flask course this month"

# Test for PUT /goals/{id} (Mark a goal as completed)
def test_mark_goal_completed():
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    # Add goal first
    response = app.test_client().post('/goals', data=json.dumps(new_goal), content_type='application/json')
    goal_id = json.loads(response.data)["id"]

    # Mark the goal as completed
    response = app.test_client().put(f'/goals/{goal_id}', content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["completed"] == True

# Test for DELETE /goals/{id} (Delete a goal)
def test_delete_goal():
    new_goal = {
        "title": "Learn Flask",
        "description": "Complete the Flask course this month"
    }
    # Add goal first
    response = app.test_client().post('/goals', data=json.dumps(new_goal), content_type='application/json')
    goal_id = json.loads(response.data)["id"]

    # Delete the goal
    response = app.test_client().delete(f'/goals/{goal_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == f"Goal 'Learn Flask' deleted"

    # Try to fetch the deleted goal
    response = app.test_client().get(f'/goals/{goal_id}')
    assert response.status_code == 404
    assert "Invalid goal ID" in str(response.data)
