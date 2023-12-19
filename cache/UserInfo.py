
from model.UserInfo import UserInfo
from utils.Redis import *

# 缓存可以在变更数据时创建，
# 暂不考虑到雪崩及穿透

CacheKey = "user"

def user_cache_list():

    f = Exists(CacheKey)
    if not f:
        userList: list[UserInfo] = UserInfo().Query()
        for u in userList:
            HSet(CacheKey, str(u.id), u.to_json())

    d = HGetAll(CacheKey)
    if len(d) <= 0:
        return []

    userList: list[UserInfo] = [UserInfo().from_json_string(v) for k,v in d.items()]
    return userList

def user_cache_select(id):

    f = HExists(CacheKey, id)
    if not f:
        user = UserInfo(id=id).Select()
        if user is not None:
            HSet(CacheKey, str(id), user.to_json())

    s = HGet(CacheKey, id)
    if s is None:
        return None

    u: UserInfo = UserInfo().from_json_string(s)
    return u


if __name__ == '__main__':
    pass
    user_cache_list()
    ul = user_cache_select(33)
    print(type(ul))
    print(ul)