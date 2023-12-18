from model.UserInfo import *
from flask import (request)


def query_user():
    # print(request.headers.get("Sec-Fetch-Dest"))
    userList: list[UserInfo] = UserInfo().Query(limit=10, offset=5)
    res = []
    for u in userList:
        res.append(u.toJson())

    return res