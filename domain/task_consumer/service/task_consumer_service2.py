from typing import Dict, Any

from domain.task_consumer.usecase.task_consumer_usecase import TaskConsumerUseCase


class TaskConsumerService2(TaskConsumerUseCase):
    def consume_task_with_processing(self, timeout_seconds: int = 5) -> Dict[str, Any]:
        pass

    def process_consumed_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        pass