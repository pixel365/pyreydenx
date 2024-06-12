from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    url: str
    expires_at: datetime


class TaskStatusChoices(str, Enum):
    PENDING = "pending"
    ERROR = "error"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ACTION_REQUIRED = "action_required"


class TaskStatus(BaseModel):
    status: TaskStatusChoices
    details: Optional[dict] = Field(default=None)


class ActionResult(BaseModel):
    request_id: Optional[str]
    order_id: Optional[int]
    action: str
    value: Optional[int]
    task: Task
