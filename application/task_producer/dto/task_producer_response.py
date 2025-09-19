from typing import Dict, Any, Optional
from pydantic import BaseModel


class TaskProducerResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Dict[str, Any]] = None


class PendingResponse(BaseModel):
    ticket: str
    pushed: int
    tasks_count: int


class ReleaseResponse(BaseModel):
    ticket: str
    released_task: Optional[Dict[str, Any]]
    success: bool


class ConsumeResponse(BaseModel):
    consumed_task: Optional[Dict[str, Any]]
    success: bool


class EnqueueResponse(BaseModel):
    ticket: str
    stage_id: str
    queue_size: int


class StatusResponse(BaseModel):
    ticket: str
    pending_count: int
    run_queue_count: int