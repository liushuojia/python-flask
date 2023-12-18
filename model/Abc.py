from model.Mysql import (
    Base,
    engine,
)
from model.DB import (
    DB,
)
from model.Model import (
    Model,
)

class Abc( Model, DB):
    __tablename__ = "abc"

    id: int = 0
    name: str = ''

if __name__ == '__main__':
    a = Abc()
    # a = Abc(id=2, name="lll", gg="abc")
    print(a)
    # print(a.toDictionary())

    # b = Abc(id=100)
    # c = Abc(id=200, pp="fff")
