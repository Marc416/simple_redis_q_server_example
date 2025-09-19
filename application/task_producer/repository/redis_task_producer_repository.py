import redis
import json
from typing import List, Optional
from domain.task_producer.entity.task_item import TaskItem
from domain.task_producer.repository.task_producer_repository import TaskProducerRepository


class RedisTaskProducerRepository(TaskProducerRepository):
    def __init__(self, redis_client: redis.Redis, run_queue_key: str = "q:run"):
        self._redis = redis_client
        self._run_queue_key = run_queue_key

    def _pending_key(self, ticket: str) -> str:
        return f"job:{ticket}:pending"

    def add_to_pending(self, ticket: str, tasks: List[TaskItem]) -> int:
        key = self._pending_key(ticket)
        pushed = 0
        for task in tasks:
            task_json = json.dumps(task.to_dict())
            result = self._redis.rpush(key, task_json)
            if result:
                pushed = result
        return pushed

    def move_pending_to_run(self, ticket: str) -> Optional[TaskItem]:
        src_key = self._pending_key(ticket)
        moved_json = self._redis.rpoplpush(src_key, self._run_queue_key)
        if moved_json:
            data = json.loads(moved_json.decode('utf-8'))
            return TaskItem.from_dict(data)
        return None

    def pop_from_run_queue(self, timeout_seconds: int = 5) -> Optional[TaskItem]:
        result = self._redis.brpop(self._run_queue_key, timeout=timeout_seconds)
        if result:
            _, task_json = result
            data = json.loads(task_json.decode('utf-8'))
            return TaskItem.from_dict(data)
        return None

    def add_to_run_queue(self, task: TaskItem) -> int:
        task_json = json.dumps(task.to_dict())
        return self._redis.rpush(self._run_queue_key, task_json)

    def get_pending_count(self, ticket: str) -> int:
        key = self._pending_key(ticket)
        return self._redis.llen(key)

    def get_run_queue_count(self) -> int:
        return self._redis.llen(self._run_queue_key)