import os
import pymysql
import redis


def connect_mysql():
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password=os.environ.get("SQL_PASSWORD"),
                           db="qq",
                           charset="utf8")
    return conn


def connect_redis():
    conn = redis.Redis()
    return conn