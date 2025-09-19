import logging
from application.task_consumer.event.task_event_broadcaster import TaskEventBroadcaster
from domain.task_consumer.usecase.task_consumer_usecase import TaskConsumerUseCase
from application.task_consumer.port.incoming.task_message_listener import TaskMessageListener

class TaskConsumerConfig:
    def __init__(self, task_consumer_usecase: TaskConsumerUseCase, timeout_seconds: int = 30):
        self._task_consumer_usecase = task_consumer_usecase
        self._timeout_seconds = timeout_seconds
        self._event_broadcaster = TaskEventBroadcaster()
        self._message_listener = TaskMessageListener(task_consumer_usecase, self._event_broadcaster)
        self._logger = logging.getLogger(__name__)

    async def start_consumer(self):
        self._logger.info("Starting task consumer...")
        await self._message_listener.start_listening(self._timeout_seconds)

    async def stop_consumer(self):
        self._logger.info("Stopping task consumer...")
        await self._message_listener.stop_listening()

    @property
    def is_running(self) -> bool:
        return self._message_listener.is_running

    @property
    def message_listener(self) -> TaskMessageListener:
        return self._message_listener

    @property
    def event_broadcaster(self) -> TaskEventBroadcaster:
        return self._event_broadcaster