import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from application.task_consumer.event.task_event_broadcaster import TaskEventBroadcaster


class WebSocketController:
    def __init__(self, event_broadcaster: TaskEventBroadcaster):
        self._event_broadcaster = event_broadcaster
        self._logger = logging.getLogger(__name__)
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_websocket_route("/ws/monitor", self.websocket_monitor)

    async def websocket_monitor(self, websocket: WebSocket):
        try:
            await self._event_broadcaster.add_connection(websocket)

            # Send initial connection message
            welcome_message = {
                "type": "connection_established",
                "message": "Connected to task monitoring",
                "active_connections": self._event_broadcaster.connection_count
            }
            await websocket.send_text(json.dumps(welcome_message))

            # Keep connection alive and handle client messages
            while True:
                try:
                    # Wait for client messages (ping/pong, etc.)
                    data = await websocket.receive_text()
                    client_message = json.loads(data)

                    if client_message.get("type") == "ping":
                        pong_message = {
                            "type": "pong",
                            "timestamp": client_message.get("timestamp")
                        }
                        await websocket.send_text(json.dumps(pong_message))

                except WebSocketDisconnect:
                    break
                except Exception as e:
                    self._logger.error(f"Error handling WebSocket message: {e}")

        except WebSocketDisconnect:
            self._logger.info("WebSocket client disconnected")
        except Exception as e:
            self._logger.error(f"WebSocket monitoring error: {e}")
        finally:
            await self._event_broadcaster.remove_connection(websocket)