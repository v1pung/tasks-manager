from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
from src.core.config import settings
from src.models import Base

TASK_SCHEMA = settings.DB_SCHEMA

task_status_enum = ENUM(
    "created", "in_progress", "completed",
    name="taskstatus",
    schema=TASK_SCHEMA,
    create_type=True
)


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(task_status_enum, default="created", nullable=False)
