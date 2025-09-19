from infrastructure.config.redis_config import RedisConfig
from application.task_producer.repository.redis_task_producer_repository import RedisTaskProducerRepository
from domain.task_producer.service.task_producer_service import TaskProducerService
from domain.task_producer.usecase.task_producer_usecase import TaskProducerUseCase
from domain.task_consumer.service.task_consumer_service import TaskConsumerService
from domain.task_consumer.usecase.task_consumer_usecase import TaskConsumerUseCase
from application.config.task_consumer_config import TaskConsumerConfig


class AppConfig:
    def __init__(self):
        self._redis_config = RedisConfig()
        self._redis_client = self._redis_config.create_client()
        self._task_repository = RedisTaskProducerRepository(self._redis_client, self._redis_config.run_queue_key)
        self._task_producer_service = TaskProducerService(self._task_repository)
        self._task_consumer_service = TaskConsumerService(self._task_producer_service)
        self._task_consumer_config = TaskConsumerConfig(self._task_consumer_service, timeout_seconds=30)


    @property
    def task_consumer_config(self) -> TaskConsumerConfig:
        return self._task_consumer_config

    @property
    def task_producer_usecase(self) -> TaskProducerUseCase:
        return self._task_producer_service

    @property
    def task_consumer_usecase(self) -> TaskConsumerUseCase:
        return self._task_consumer_service