from flask import Flask 
from users import user_list

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'welcome to the party'

@app.route('/users')
def get_users():
    users = list(user_list.values())
    return users

if __name__ == '__main__':
    app.run(debug=True)
