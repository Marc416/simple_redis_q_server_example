import asyncio
import json
import logging
from typing import Set, Dict, Any
from fastapi import WebSocket


class TaskEventBroadcaster:
    def __init__(self):
        self._connections: Set[WebSocket] = set()
        self._logger = logging.getLogger(__name__)

    async def add_connection(self, websocket: WebSocket):
        await websocket.accept()
        self._connections.add(websocket)
        self._logger.info(f"WebSocket connection added. Total connections: {len(self._connections)}")

    async def remove_connection(self, websocket: WebSocket):
        if websocket in self._connections:
            self._connections.remove(websocket)
            self._logger.info(f"WebSocket connection removed. Total connections: {len(self._connections)}")

    async def broadcast_task_processed(self, result: Dict[str, Any]):
        if not self._connections:
            return

        message = {
            "type": "task_processed",
            "timestamp": result.get("timestamp"),
            "data": result
        }

        disconnected = set()
        for websocket in self._connections:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                self._logger.warning(f"Failed to send message to WebSocket: {e}")
                disconnected.add(websocket)

        # Remove disconnected connections
        for websocket in disconnected:
            self._connections.discard(websocket)

    async def broadcast_status(self, status: Dict[str, Any]):
        if not self._connections:
            return

        message = {
            "type": "status_update",
            "data": status
        }

        disconnected = set()
        for websocket in self._connections:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                self._logger.warning(f"Failed to send status to WebSocket: {e}")
                disconnected.add(websocket)

        # Remove disconnected connections
        for websocket in disconnected:
            self._connections.discard(websocket)

    @property
    def connection_count(self) -> int:
        return len(self._connections)