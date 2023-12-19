# app.py
import datetime
import threading
import time

from flask import Flask
from flask import (request, make_response)
from utils.Redis import Subscribe, Publish
from api.UserInfo import (
    query_user,
    create_user,
    get_user_by_id,
    update_user_by_id,
    delete_user_by_id,
    cache_user,
    select_cache_user,
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
# user cache
app.add_url_rule('/cache/user', methods=['GET'], view_func=cache_user)
app.add_url_rule('/cache/user/<int:id>', methods=['GET'], view_func=select_cache_user)

def subscribeCallback(message):
    print(message)

def SubscribeAction():
    Subscribe(["int_channel", "aa"], subscribeCallback)

def PublishAction():
    for i in range(10):
        Publish("int_channel", i * 2)
        print(f"生产: {i * 2}")
        time.sleep(2)


if __name__ == '__main__':
    subscribe = threading.Thread(target=SubscribeAction, daemon=True)
    # 启动线程
    subscribe.start()

    # publish = threading.Thread(target=PublishAction, daemon=True)
    # # 启动线程
    # publish.start()

    app.run(host="127.0.0.1", port=8080, debug=True)
