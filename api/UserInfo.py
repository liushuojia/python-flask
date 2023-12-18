import json

from model.UserInfo import UserInfo
from flask import (request, make_response)


def query_user():
    # print(request.headers.get("Sec-Fetch-Dest"))
    userList: list[UserInfo] = UserInfo().Query(limit=10, offset=5)
    res = []
    for u in userList:
        res.append(u.toJson())

    return res

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

def get_user_by_id(id):

    u:UserInfo = UserInfo().Select(id)

    if u is not None:
        return u.toJson()

    return "数据不存在"


def update_user_by_id(id):
    request_str = request.get_data()
    request_dict = json.loads(request_str)

    u:UserInfo = UserInfo(id=id).Select()
    if u is None:
        return make_response("not found", 400)

    flag = u.Update(request_dict)
    if flag:
        return make_response("update success", 200)

    return make_response("update fail", 500)

def delete_user_by_id(id):

    u: UserInfo = UserInfo(id=id).Select()
    if u is None:
        return make_response("not found", 400)

    flag = u.Delete(id)
    if flag:
        return make_response("delete success", 200)

    return make_response("delete fail", 500)