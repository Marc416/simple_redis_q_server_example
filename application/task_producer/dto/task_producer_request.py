from typing import List, Dict, Any
from pydantic import BaseModel


class TaskItemRequest(BaseModel):
    stage_id: str
    payload: Dict[str, Any] = {}


class PendingBatchRequest(BaseModel):
    items: List[TaskItemRequest] = []


class RunEnqueueRequest(BaseModel):
    ticket: str
    stage_id: str
    payload: Dict[str, Any] = {}