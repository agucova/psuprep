import os
from huey import RedisHuey

tareas = RedisHuey(url=os.environ.get("REDIS_URL"))
