import numpy as np


def circular_store(redis, stat_name, stat_value):
    stat_value = np.average(np.append(np.asfarray(redis.lrange(stat_name, 0, 1)), stat_value))

    redis.lpush(stat_name, stat_value)
    redis.ltrim(stat_name, 0, 100)


def circular_all(redis, stat_name):
    return np.asfarray(redis.lrange(stat_name, 0, 100), float).tolist()