# app.py
import datetime

from flask import Flask
from flask import (request, make_response)
import json
from model.UserInfo import *
from api.UserInfo import query_user

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

# get /user
app.add_url_rule('/user', methods=['GET'], view_func=query_user)
# @app.route('/user', methods=['GET'])
# def query_user():
#     userList: list[UserInfo] = UserInfo().Query(limit=10, offset=5)
#     res = []
#     for u in userList:
#         res.append(u.toJson())
#
#     return res



@app.route('/user', methods=['POST'])
def create_user():
    request_str = request.get_data()
    request_dict = json.loads(request_str)

    u = UserInfo.fromJson(request_dict)
    print(request_str)
    print(request_dict)
    print(u.id)
    print(u.name)

    u.Create()


    # user = UserInfo(
    #     id=0,
    #     name="刘硕嘉"
    # )
    # print(user)
    # user.create()

    # response = Response("create_user")
    # response.status_code = 200
    # response.status = "200 Ok"
    # response.data = request_dict
    return make_response(request_dict,200)


@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):

    user: UserInfo = UserInfo()
    u: UserInfo = user.Select(id)

    if u is not None:
        return u.toJson()

    return "数据不存在"


@app.route('/user/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    return '%d\'s id' % id


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
