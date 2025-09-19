import logging
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.config.app_config import AppConfig
from application.websocket.websocket_controller import WebSocketController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_config = AppConfig()

app = FastAPI(title="Simple Queue Server", version="1.0.0")

# Task consumer runs in separate process (consumer.py)

from application.task_producer.controller.task_producer_controller import router as task_producer_router
app.include_router(task_producer_router)

websocket_controller = WebSocketController(app_config.task_consumer_config.event_broadcaster)
app.include_router(websocket_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
