# app.py
import datetime

from flask import Flask
from flask import (request, make_response)
import json
from model.UserInfo import *
from api.UserInfo import (
    query_user,
    create_user,
    get_user_by_id,
    update_user_by_id,
    delete_user_by_id,
)

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

# user
app.add_url_rule('/user', methods=['GET'], view_func=query_user)
app.add_url_rule('/user', methods=['POST'], view_func=create_user)
app.add_url_rule('/user/<int:id>', methods=['GET'], view_func=get_user_by_id)
app.add_url_rule('/user/<int:id>', methods=['PUT'], view_func=update_user_by_id)
app.add_url_rule('/user/<int:id>', methods=['DELETE'], view_func=delete_user_by_id)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
