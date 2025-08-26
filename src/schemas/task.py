from pydantic import BaseModel, UUID4, ConfigDict
from typing import Optional
from enum import StrEnum


class TaskStatus(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: UUID4
