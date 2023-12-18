import datetime
import json
import time

from werkzeug.routing import ValidationError

from utils.Mysql import (
    Base,
    engine,
    Session,
    DB,
)
from sqlalchemy.orm import scoped_session

def Create(v, session = None):
    # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
    # 内部会采用threading.local进行隔离
    v.create_time = datetime.datetime.now()
    v.last_update_time = datetime.datetime.now()
    v.id = None

    if session is None:
        session = scoped_session(Session)
        try:
            session.add(v)
            session.flush()
            session.commit()
            return v.id
        except ValidationError as e:
            print(e)
        finally:
            session.remove()
    else:
        try:
            session.add(v)
            session.flush()
            return v.id
        except ValidationError as e:
            print(e)
        finally:
            pass
    return 0

def Update(info, id: int, v, session = None):
    if id <= 0:
        return False

    del v["create_time"]
    v["last_update_time"] = datetime.datetime.now()

    if session is None:
        session = scoped_session(Session)
        n = session.query(info) \
            .filter(info.id == id) \
            .update(v)

        session.commit()
        session.remove()
        return n == 1
    else:
        n = session.query(info) \
            .filter(info.id == id) \
            .update(v)
        return n == 1

def Delete(info, id: int, session = None):
    if id <= 0:
        return False

    if session is None:
        session = scoped_session(Session)
        n = session.query(info) \
            .filter(info.id == id) \
            .delete()

        session.commit()
        session.remove()
        return n == 1
    else:
        n = session.query(info) \
            .filter(info.id == id) \
            .delete()
        return n == 1

def Select(info, id: int, session = None):
    if id <= 0:
        return None

    if session is None:
        session = scoped_session(Session)
        data = session.query(info) \
            .filter(info.id == id) \
            .first()

        session.commit()
        session.remove()
        return data
    else:
        data = session.query(info) \
            .filter(info.id == id) \
            .first()
        return data

def Query(info, filter=None, limit:int = 0, offset: int = 0, session = None):
    if session is None:
        session = scoped_session(Session)
        q = session.query(info)
        if filter is not None:
            q = q.filter(filter)
        if offset > 0:
            q = q.offset(offset)
        if limit > 0:
            q = q.limit(limit)

        dataList = q.all()

        session.commit()
        session.remove()
        return dataList
    else:
        q = session.query(info)
        if filter is not None:
            q = q.filter(filter)
        if offset > 0:
            q = q.offset(offset)
        if limit > 0:
            q = q.limit(limit)

        return q.all()

class DB:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return json.dumps(self.toJson())

    def toJson(self):
        mappings = dict()
        for key in list(self.__dict__.keys()):
            if key.startswith("_"): continue
            v = getattr(self, key)
            if isinstance(v, datetime.datetime):
                if v is not None:
                    mappings[key] = v.strftime("%Y-%m-%d %H:%M:%S")
                continue
            if v is not None:
                mappings[key] = v

        return mappings
    def prt(self):
        print(self.__class__)

    def Create(self, session = None):
        return Create(self, session)

    def Update(self, info, id = None, session = None):
        if id is not None:
            Update(self.__class__, id, info, session)

        return Update(self.__class__, self.id, info, session)

    def Delete(self, id: int, session = None):
        return Delete(self.__class__, id, session)

    def Select(self, id = None, session = None):
        if id is not None:
            return Select(self.__class__, id, session)

        return Select(self.__class__, self.id, session)

    def Query(self, filter = None, limit: int = 0, offset: int = 0, session = None):
        return Query(self.__class__, filter, limit, offset, session)