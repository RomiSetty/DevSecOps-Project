from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Goal class
class Goal:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
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

    def mark_goal_completed(self, index):
        if 0 <= index < len(self.goals):
            self.goals[index].mark_completed()
            return True
        return False

    def delete_goal(self, index):
        if 0 <= index < len(self.goals):
            return self.goals.pop(index)
        return None

    def show_goal_details(self, index):
        if 0 <= index < len(self.goals):
            return self.goals[index].to_dict()
        return None

# Initialize Goal Tracker
tracker = GoalTracker()

# Routes
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

@app.route('/goals', methods=['POST'])
def add_goal():
    data = request.json
    if "title" not in data or "description" not in data:
        return jsonify({"error": "Title and description required"}), 400
    goal = tracker.add_goal(data["title"], data["description"])
    return jsonify(goal.to_dict()), 201

@app.route('/goals/<int:goal_id>', methods=['PUT'])
def mark_goal_completed(goal_id):
    if tracker.mark_goal_completed(goal_id):
        return jsonify({"message": "Goal marked as completed"})
    return jsonify({"error": "Invalid goal ID"}), 404

@app.route('/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = tracker.delete_goal(goal_id)
    if goal:
        return jsonify({"message": f"Goal '{goal.title}' deleted"})
    return jsonify({"error": "Invalid goal ID"}), 404

@app.route('/goals/<int:goal_id>', methods=['GET'])
def show_goal_details(goal_id):
    goal = tracker.show_goal_details(goal_id)
    if goal:
        return jsonify(goal)
    return jsonify({"error": "Invalid goal ID"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
