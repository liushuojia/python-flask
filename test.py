
import json
from decimal import Decimal
from datetime import datetime

from model.UserInfo import UserInfo
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)

if __name__ == '__main__':

    j = """{
    "id": 1,
    "name": "\u5927\u70e7\u997c",
    "age": 20,
    "phone": "13725588389",
    "gender": "male",
    "create_time": "2023-12-19 10:31:18",
    "last_update_time": null,
    "delete_status": true
}"""
    print(json.loads(j))
    print(UserInfo().from_json_string(j))

    exit(0)

    u = UserInfo()
    u.id = 1
    u.name = "大烧饼"
    u.age = 20
    u.phone = "13725588389"
    u.gender = "male"
    u.create_time = datetime.now()
    u.last_update_time = None
    u.delete_status = True

    print(u.to_json(4))

    t = u.to_dict()
    print(t)
    for i in t:
        print(i, t[i])


    res = json.dumps(t, cls=MyJSONEncoder, indent=4)
    print(res)
