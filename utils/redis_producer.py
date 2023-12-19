from utils.Redis import *
import time

def producer():
    for i in range(10):
        Publish("aa", i*2)
        print(f"生产: {i*2}")
        time.sleep(2)

if __name__ == "__main__":
    producer()