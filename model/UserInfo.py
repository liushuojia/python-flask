# UserInfo.py
# from typing import Optional
import json

from utils.Mysql import (
    Base,
    engine,
)
from utils.DB import (
    DB,
    Create,
    Select,
    Update,
    Delete,
    Query,
)
import datetime
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


class UserInfo(Base, DB):
    """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "userInfo"

    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(32), index=True, nullable=False, comment="姓名")
    age = Column(Integer, nullable=False, comment="年龄")
    # phone = Column(String(11), nullable=False, unique=True, comment="手机号")
    phone = Column(String(11), nullable=False, comment="手机号")
    address = Column(String(64), nullable=False, comment="地址")

    # 对于非必须插入的字段，不用采取nullable=False进行约束
    gender = Column(Enum("male", "female"), default="male", comment="性别")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    last_update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")
    delete_status = Column(Boolean(), default=False, comment="是否删除")

    __table__args__ = (
        UniqueConstraint("name", "age"),  # 联合唯一约束
        Index("name", "addr", unique=True),       # 联合唯一索引
    )


if __name__ == "__main__":
    # 删除表
    Base.metadata.drop_all(engine)
    # 创建表
    Base.metadata.create_all(engine)
