import redis
from typing import Optional


class RedisConfig:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        run_queue_key: str = "q:run"
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.run_queue_key = run_queue_key

    def create_client(self) -> redis.Redis:
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=False
        )