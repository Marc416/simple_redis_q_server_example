import asyncio
import logging
from datetime import datetime
from typing import Optional

from application.task_consumer.event.task_event_broadcaster import TaskEventBroadcaster
from domain.task_consumer.usecase.task_consumer_usecase import TaskConsumerUseCase


class TaskMessageListener:
    def __init__(self, task_consumer_usecase: TaskConsumerUseCase, event_broadcaster: TaskEventBroadcaster):
        self._task_consumer_usecase = task_consumer_usecase
        self._event_broadcaster = event_broadcaster
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._logger = logging.getLogger(__name__)

    async def start_listening(self, timeout_seconds: int = 30):
        if self._running:
            self._logger.warning("Message listener is already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._listen_loop(timeout_seconds))
        self._logger.info("Task message listener started")

    async def stop_listening(self):
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._logger.info("Task message listener stopped")

    async def _listen_loop(self, timeout_seconds: int):
        self._logger.info(f"Starting message listener with {timeout_seconds}s blocking timeout")

        while self._running:
            try:
                result = self._task_consumer_usecase.consume_task_with_processing(timeout_seconds=timeout_seconds)

                if result["success"]:
                    await self._handle_message_processed(result)
                else:
                    self._logger.debug("No messages available, blocking for next message...")

            except Exception as e:
                self._logger.error(f"Error in message listener loop: {e}")
                await asyncio.sleep(1)

    async def _handle_message_processed(self, result: dict):
        # Add timestamp to result
        result["timestamp"] = datetime.now().isoformat()

        self._logger.info(f"Message processed: {result['type']}")

        if "original_task" in result:
            task_info = result["original_task"]
            self._logger.info(
                f"Task details - Ticket: {task_info.get('ticket')}, "
                f"Stage: {task_info.get('stageId')}, "
                f"Processed at: {result.get('processed_result', {}).get('processed_at')}"
            )

        if "processed_result" in result:
            processed_info = result["processed_result"]
            self._logger.info(f"Processing result: {processed_info}")

        # Broadcast to all WebSocket connections
        await self._event_broadcaster.broadcast_task_processed(result)

    @property
    def is_running(self) -> bool:
        return self._running
