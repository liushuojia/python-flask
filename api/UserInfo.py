import json
import math

from model.UserInfo import UserInfo
from flask import (request, make_response)
from sqlalchemy import and_, or_
from cache.UserInfo import (
    user_cache_list,
    user_cache_select,
)

def query_user():
    # print(request.headers.get("Sec-Fetch-Dest"))


    page = request.args.get("page")
    try:
        page = int(page)
        if page < 0:
            page = 1
    except:
        page = 1


    pageSize = request.args.get("pageSize")
    try:
        pageSize = int(pageSize)
        if pageSize < 0:
            pageSize = 30
    except:
        pageSize = 30

    offset = (page-1)*pageSize

    # filter = UserInfo.id==28
    # filter = or_(UserInfo.id==28, UserInfo.id==29)
    # filter = or_(UserInfo.name.like("%liu%"), UserInfo.address.like("%深圳市%"))
    # filter = and_(UserInfo.name.like("%liu%"), UserInfo.address.like("%深圳市%"))
    filter = and_(
        UserInfo.name.like("%liu%"),
        UserInfo.address.like("%深圳市%"),
        or_(
            UserInfo.id==24,
            UserInfo.id==26,
        )
    )

    searchList = []
    name_like = request.args.get("name_like")
    if name_like:
        searchList.append(UserInfo.name.like("%"+name_like+"%"))

    address_like = request.args.get("address_like")
    if address_like:
        searchList.append(UserInfo.address.like("%" + address_like +"%"))

    filter = None
    if len(searchList) > 0:
        filter = and_(v for v in searchList if v is not None)

    userInfo = UserInfo()
    userList: list[UserInfo] = userInfo.Query(
        limit=pageSize,
        offset=offset,
        filter=filter,
    )
    totalSize = userInfo.Count(filter=filter)

    res = [u.to_dict() for u in userList]
    return {
        "page": page,
        "pageSize": pageSize,
        "totalSize": totalSize,
        "totalPage": math.ceil(float(totalSize)/float(pageSize)),
        "data": res,
    }

def create_user():
    request_str = request.get_data()
    # request_dict = json.loads(request_str)

    u: UserInfo = UserInfo().from_json_string(request_str)

    id = u.Create()
    if id > 0:
        return "创建成功"

    return str(u.Create())

def get_user_by_id(id):

    u:UserInfo = UserInfo(id=id).Select()

    if u is not None:
        return u.to_dict()

    return make_response("创建失败", 400)


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

    flag = u.Delete()
    if flag:
        return make_response("delete success", 200)

    return make_response("delete fail", 500)


def cache_user():
    userList = user_cache_list()
    res = [u.to_dict() for u in userList]
    return res

def select_cache_user(id):
    user = user_cache_select(id)
    return user.to_dict()
