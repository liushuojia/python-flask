import redis

HOST = "127.0.0.1"
PORT = 6379
MAXCONNECTIONS = 10
DB = 1
PASSWORD = "liushuojia"

#创建连接池并连接到redis，并设置最大连接数量;
conn_pool = redis.ConnectionPool(
    host=HOST,
    port=PORT,
    max_connections=MAXCONNECTIONS,
    db=DB,
    password=PASSWORD
)

def Conn():
    return redis.Redis(
        connection_pool=conn_pool,
    )

def get(key:str):
    return Conn().get(key)

def exists(key:str):
    return Conn().exists(key)

def set(key:str, value):
    return Conn().set(key, value)


if __name__ == '__main__':
    print(get("a"))
    print(set("a","0001"))
    print(get("a"))
    print(exists("a"))
