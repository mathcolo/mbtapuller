import Database
import Functions


def circular_store(redis, stat_name, stat_value):
    redis.lpush(stat_name, stat_value)
    redis.ltrim(stat_name, 0, 9)


def circular_all(redis, stat_name):
    return redis.lrange(stat_name, 0, 9)