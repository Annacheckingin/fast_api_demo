import redis.asyncio as redis
from redis.exceptions import ConnectionError,TimeoutError

redis_pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    db=0,
    max_connections=10,
    decode_responses=True
)

