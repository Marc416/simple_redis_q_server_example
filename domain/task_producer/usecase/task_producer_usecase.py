from abc import ABC, abstractmethod
from typing import List


class TaskProducerUseCase(ABC):

    @abstractmethod
    def add_pending_tasks(self, ticket: str, stage_ids: List[str], payloads: List[dict]) -> dict:
        pass

    @abstractmethod
    def release_task_to_run(self, ticket: str) -> dict:
        pass

    @abstractmethod
    def consume_next_task(self, timeout_seconds: int = 5) -> dict:
        pass

    @abstractmethod
    def enqueue_direct_run(self, ticket: str, stage_id: str, payload: dict) -> dict:
        pass

    @abstractmethod
    def get_queue_status(self, ticket: str) -> dict:
        pass