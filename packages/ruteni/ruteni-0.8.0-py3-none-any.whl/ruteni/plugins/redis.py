import aioredis
from ruteni.config import config

REDIS_URL: str = config.get(
    "RUTENI_REDIS_URL", default="redis+unix:///run/redis/redis-server.sock"
)

redis = aioredis.from_url(REDIS_URL)
