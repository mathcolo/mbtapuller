import numpy as np


def circular_store(redis, stat_name, stat_value):
    redis.lpush(stat_name, stat_value)
    redis.ltrim(stat_name, 0, 100)


def circular_all(redis, stat_name):
    return np.asfarray(redis.lrange(stat_name, 0, 100), float).tolist()