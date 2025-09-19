from typing import Dict, Any, Optional
from datetime import datetime


class TaskItem:
    def __init__(self, ticket: str, stage_id: str, payload: Dict[str, Any], created_at: Optional[datetime] = None):
        self.ticket = ticket
        self.stage_id = stage_id
        self.payload = payload
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket": self.ticket,
            "stageId": self.stage_id,
            "payload": self.payload,
            "createdAt": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskItem':
        return cls(
            ticket=data["ticket"],
            stage_id=data["stageId"],
            payload=data.get("payload", {}),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None
        )