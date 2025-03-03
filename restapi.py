from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Goal class
class Goal:
    def __init__(self, title, description, id=None):
        self.id = id if id else self.generate_id()  # Unique ID
        self.title = title
        self.description = description
        self.completed = False

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())  # Generate a unique identifier using UUID

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

# Goal Tracker class
class GoalTracker:
    def __init__(self):
        self.goals = []

    def add_goal(self, title, description):
        new_goal = Goal(title, description)
        self.goals.append(new_goal)
        return new_goal

    def list_goals(self):
        return [goal.to_dict() for goal in self.goals]

    def mark_goal_completed(self, goal_id):
        goal = self.get_goal_by_id(goal_id)
        if goal:
            goal.mark_completed()
            return True
        return False

    def delete_goal(self, goal_id):
        goal = self.get_goal_by_id(goal_id)
        if goal:
            self.goals.remove(goal)
            return goal
        return None

    def show_goal_details(self, goal_id):
        goal = self.get_goal_by_id(goal_id)
        if goal:
            return goal.to_dict()
        return None

    def get_goal_by_id(self, goal_id):
        return next((goal for goal in self.goals if goal.id == goal_id), None)

# Initialize Goal Tracker
tracker = GoalTracker()

# Home route
@app.route('/')
def home():
    return "Welcome to the Goal Tracking API!"

# List all goals in HTML format
@app.route('/goals', methods=['GET'])
def list_goals():
    goals = tracker.list_goals()
    goals_html = '<ul>'
    for goal in goals:
        goals_html += f"<li>{goal['title']} - {'Completed' if goal['completed'] else 'In Progress'}</li>"
    goals_html += '</ul>'
    return render_template_string(goals_html)

# Add a new goal
@app.route('/goals', methods=['POST'])
def add_goal():
    data = request.json
    if "title" not in data or "description" not in data:
        return jsonify({"error": "Title and description required"}), 400
    goal = tracker.add_goal(data["title"], data["description"])
    return jsonify(goal.to_dict()), 201

# Mark a goal as completed
@app.route('/goals/<string:goal_id>', methods=['PUT'])
def mark_goal_completed(goal_id):
    if tracker.mark_goal_completed(goal_id):
        return jsonify({"message": "Goal marked as completed"})
    return jsonify({"error": f"Goal with ID {goal_id} not found"}), 404

# Delete a goal
@app.route('/goals/<string:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = tracker.delete_goal(goal_id)
    if goal:
        return jsonify({"message": f"Goal '{goal.title}' deleted"})
    return jsonify({"error": f"Goal with ID {goal_id} not found"}), 404

# Show goal details
@app.route('/goals/<string:goal_id>', methods=['GET'])
def show_goal_details(goal_id):
    goal = tracker.show_goal_details(goal_id)
    if goal:
        return jsonify(goal)
    return jsonify({"error": f"Goal with ID {goal_id} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
