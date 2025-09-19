from typing import Dict, Any, Optional
from pydantic import BaseModel


class TaskConsumerResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Dict[str, Any]] = None


class ConsumeResponse(BaseModel):
    consumed_task: Optional[Dict[str, Any]]
    success: bool