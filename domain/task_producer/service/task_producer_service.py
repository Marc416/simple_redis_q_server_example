from typing import List, Optional
from domain.task_producer.entity.task_item import TaskItem
from domain.task_producer.repository.task_producer_repository import TaskProducerRepository
from domain.task_producer.usecase.task_producer_usecase import TaskProducerUseCase


class TaskProducerService(TaskProducerUseCase):
    def __init__(self, task_repository: TaskProducerRepository):
        self._task_repository = task_repository

    def add_pending_tasks(self, ticket: str, stage_ids: List[str], payloads: List[dict]) -> dict:
        tasks = []
        for i, stage_id in enumerate(stage_ids):
            payload = payloads[i] if i < len(payloads) else {}
            task = TaskItem(ticket=ticket, stage_id=stage_id, payload=payload)
            tasks.append(task)

        pushed = self._add_pending_batch(ticket, tasks)
        return {
            "ticket": ticket,
            "pushed": pushed,
            "tasks_count": len(tasks)
        }

    def release_task_to_run(self, ticket: str) -> dict:
        task = self._release_one_task(ticket)
        return {
            "ticket": ticket,
            "released_task": task.to_dict() if task else None,
            "success": task is not None
        }

    def consume_next_task(self, timeout_seconds: int = 5) -> dict:
        task = self._consume_task(timeout_seconds)
        return {
            "consumed_task": task.to_dict() if task else None,
            "success": task is not None
        }

    def enqueue_direct_run(self, ticket: str, stage_id: str, payload: dict) -> dict:
        task = TaskItem(ticket=ticket, stage_id=stage_id, payload=payload)
        queue_size = self._enqueue_run_task(task)
        return {
            "ticket": ticket,
            "stage_id": stage_id,
            "queue_size": queue_size
        }

    def get_queue_status(self, ticket: str) -> dict:
        stats = self._get_queue_stats(ticket)
        return {
            "ticket": ticket,
            **stats
        }

    def _add_pending_batch(self, ticket: str, tasks: List[TaskItem]) -> int:
        return self._task_repository.add_to_pending(ticket, tasks)

    def _release_one_task(self, ticket: str) -> Optional[TaskItem]:
        return self._task_repository.move_pending_to_run(ticket)

    def _consume_task(self, timeout_seconds: int = 5) -> Optional[TaskItem]:
        return self._task_repository.pop_from_run_queue(timeout_seconds)

    def _enqueue_run_task(self, task: TaskItem) -> int:
        return self._task_repository.add_to_run_queue(task)

    def _get_queue_stats(self, ticket: str) -> dict:
        return {
            "pending_count": self._task_repository.get_pending_count(ticket),
            "run_queue_count": self._task_repository.get_run_queue_count()
        }