from abc import ABC, abstractmethod
from typing import List, Optional
from domain.task_producer.entity.task_item import TaskItem


class TaskProducerRepository(ABC):

    @abstractmethod
    def add_to_pending(self, ticket: str, tasks: List[TaskItem]) -> int:
        pass

    @abstractmethod
    def move_pending_to_run(self, ticket: str) -> Optional[TaskItem]:
        pass

    @abstractmethod
    def pop_from_run_queue(self, timeout_seconds: int = 5) -> Optional[TaskItem]:
        pass

    @abstractmethod
    def add_to_run_queue(self, task: TaskItem) -> int:
        pass

    @abstractmethod
    def get_pending_count(self, ticket: str) -> int:
        pass

    @abstractmethod
    def get_run_queue_count(self) -> int:
        pass