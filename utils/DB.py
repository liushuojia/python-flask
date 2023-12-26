from datetime import datetime, date
import json

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
    v.create_time = datetime.now()
    v.last_update_time = datetime.now()
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
    v["last_update_time"] = datetime.now()

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

def Delete(info, id:int, session=None):
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

def Select(info, id:int, session=None):
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

def Query(info, filter=None, limit:int=0, offset:int=0, session=None):
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

def Count(info, filter=None, session=None):
    if session is None:
        session = scoped_session(Session)
        q = session.query(info)
        if filter is not None:
            q = q.filter(filter)

        n = q.count()

        session.commit()
        session.remove()
        return n
    else:
        q = session.query(info)
        if filter is not None:
            q = q.filter(filter)

        return q.count()

class DB:

    id: int = 0
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)

    def to_dict(self):
        mappings = dict()
        for key in list(self.__dict__.keys()):
            if key.startswith("_"):
                continue
            v = getattr(self, key)
            if v is None:
                mappings[key] = None
                continue
            if isinstance(v, datetime):
                mappings[key] = v.strftime("%Y-%m-%d %H:%M:%S")
                continue
            if isinstance(v, date):
                mappings[key] = v.strftime("%Y-%m-%d")
                continue
            if isinstance(v, bytes):
                mappings[key] = str(v, encoding="utf-8")
                continue
            # if isinstance(v, int):
            #     mappings[key] = int(v)
            #     continue
            if isinstance(v, float):
                mappings[key] = float(v)
                continue
            if isinstance(v, bool):
                mappings[key] = bool(v)
                continue

            # int str
            mappings[key] = v

        return mappings

    def from_json_string(self, s):
        return self.from_json(json.loads(s))

    def from_json(self, o):
        for key, value in o.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self

    def Create(self, session=None):
        return Create(self, session)

    def Update(self, info, session=None):
        return Update(self.__class__, self.id, info, session)

    def Delete(self, session=None):
        return Delete(self.__class__, self.id, session)

    def Select(self, session=None):
        return Select(self.__class__, self.id, session)

    def Query(self, filter=None, limit: int = 0, offset: int = 0, session=None):
        return Query(self.__class__, filter, limit, offset, session)

    def Count(self, filter=None, session=None):
        return Count(self.__class__, filter, session)
