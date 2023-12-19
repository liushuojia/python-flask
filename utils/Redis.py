import threading
import time
from typing import Optional, Union

import redis

# =============================================
HOST = "127.0.0.1"
PORT = 6379
MAXCONNECTIONS = 10
DB = 1
PASSWORD = "liushuojia"
# =============================================

# 创建连接池并连接到redis，并设置最大连接数量;
conn_pool = redis.ConnectionPool(
    host=HOST,
    port=PORT,
    max_connections=MAXCONNECTIONS,
    db=DB,
    password=PASSWORD,
    decode_responses=True,
    # health_check_interval=30,
)

# 这里简单封装了下， 防止不同版本的redis库调整后去影响业务代码
def Conn():
    wait = False
    while True:
        try:
            if wait:
                time.sleep(5)

            r = redis.Redis(connection_pool=conn_pool)
            r.ping()
        except Exception as e:
            print('redis连接失败,正在尝试重连')
            print(e)
            wait = True
            continue
        else:
            return r

def Ping():
    return Conn().ping()

def Get(key:str):
    return Conn().get(key)

def Exists(key:str):
    return Conn().exists(key)

def Set(key:str, value):
    return Conn().set(key, value)

def Delete(key:str):
    return Conn().delete(key)

def Expire(key:str, second:int):
    return Conn().expire(key, second)

def TTL(key:str):
    return Conn().ttl(key)

def LPush(key:str, *args):
    return Conn().lpush(key,*args)

def LPop(key:str):
    return Conn().lpop(key)

def BLPop(key:str):
    return Conn().blpop(key)

def RPush(key:str, *args):
    return Conn().rpush(key,*args)

def RPop(key:str):
    return Conn().rpop(key)

def BRPop(key:str):
    return Conn().brpop(key)

def LLen(key:str):
    return Conn().llen(key)

def SAdd(key:str, *args):
    return Conn().sadd(key, *args)

def SCard(key:str):
    return Conn().scard(key)

def SRem(key:str, *args):
    return Conn().srem(key,*args)

def SRandMember(key:str, count = None):
    return Conn().srandmember(key, count)

def SMember(key:str):
    return Conn().smembers(key)

def SIsMember(key:str, value):
    return Conn().sismember(key, value)

def HSet(name:str, key:str, value):
    return Conn().hset(name, key, value)

def HSetDict(name:str, field:dict):
    return Conn().hset(name=name, mapping=field)

def HSetNX(name:str, key:str, value):
    return Conn().hsetnx(name, key, value)

def HGetAll(name:str):
    return Conn().hgetall(name)

def HKeys(name:str):
    return Conn().hkeys(name)

def HDel(name:str, *keys):
    return Conn().hdel(name, keys)

def HExists(name:str, key: str):
    return Conn().hexists(name, key)

def HGet(name:str, key: str):
    return Conn().hget(name, key)

def HLen(name:str):
    return Conn().hlen(name)

def Publish(channel:str, message):
    return Conn().publish(channel, message)

def Subscribe(channel: Union[str, list[str]], func):
    while True:
        try:
            c = Conn()
            pub = c.pubsub()

            if channel is list:
                for msg in channel:
                    pub.subscribe(msg)
            else:
                pub.subscribe(channel)

            msg_stream = pub.listen()
            for msg in msg_stream:
                if msg["type"] == "message":
                    print(str(msg["channel"]) + ": " + str(msg["data"]))
                    func(msg["data"])
                elif msg["type"] == "subscribe":
                    print(str(msg["channel"]), "订阅成功")

        except Exception as e:
            print('订阅发生错误', e)


def workerCB(message):
    print(message)

def worker():
    Subscribe(["int_channel", "aa"], workerCB)

if __name__ == '__main__':
    pass
    t = threading.Thread(target=worker, daemon=True)
    # 启动线程
    t.start()

    for i in range(10):
        Publish("aa", i * 2)
        print(f"生产: {i * 2}")
        time.sleep(2)

    # LPush("a",1,2,3,4,5,)
    # LPush("a","A","B","C","D","E","F")
    # LPop("a")

    # SAdd("a11",1,2,3,4)
    # v = SRandMember("a11", 4)
    # print(v, type(v))
    # print(LPop("a", 3))

