from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class TaskConsumerUseCase(ABC):

    @abstractmethod
    def consume_task_with_processing(self, timeout_seconds: int = 5) -> Dict[str, Any]:
        pass

    @abstractmethod
    def process_consumed_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        pass