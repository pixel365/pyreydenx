from datetime import datetime
from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    url: str
    expires_at: datetime


class TaskStatusChoices(StrEnum):
    PENDING = auto()
    ERROR = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    ACTION_REQUIRED = auto()


class TaskStatus(BaseModel):
    status: TaskStatusChoices
    details: Optional[dict] = Field(default=None)


class ActionResult(BaseModel):
    request_id: Optional[str]
    order_id: Optional[int]
    action: str
    value: Optional[int]
    task: Task
