from typing import Dict, Any
from domain.task_consumer.usecase.task_consumer_usecase import TaskConsumerUseCase
from domain.task_producer.usecase.task_producer_usecase import TaskProducerUseCase


class TaskConsumerService(TaskConsumerUseCase):
    def __init__(self, task_usecase: TaskProducerUseCase):
        self._task_usecase = task_usecase

    def consume_task_with_processing(self, timeout_seconds: int = 5) -> Dict[str, Any]:
        result = self._task_usecase.consume_next_task(timeout_seconds)

        if result["success"]:
            task_data = result["consumed_task"]
            processed_result = self.process_consumed_task(task_data)
            return {
                "type": "task_processed",
                "success": True,
                "original_task": task_data,
                "processed_result": processed_result
            }
        else:
            return {
                "type": "no_task",
                "success": False,
                "message": "No tasks available in queue"
            }

    def process_consumed_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "processed_at": task_data.get("createdAt"),
            "ticket": task_data.get("ticket"),
            "stage_id": task_data.get("stageId"),
            "payload_size": len(str(task_data.get("payload", {}))),
            "status": "processed"
        }