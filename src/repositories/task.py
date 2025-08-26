import logging
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from uuid import UUID
from typing import List, Optional

logger = logging.getLogger("src")


class AbstractTaskRepository(ABC):
    @abstractmethod
    async def create(self, task: TaskCreate) -> Task:
        pass

    @abstractmethod
    async def get(self, task_id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_list(self, skip: int = 0, limit: int = 100) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        pass

    @abstractmethod
    async def delete(self, task_id: UUID) -> bool:
        pass


class TaskRepository(AbstractTaskRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task: TaskCreate) -> Task:
        logger.debug(f"Creating task with title={task.title}")
        db_task = Task(**task.model_dump())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        logger.info(f"Task created with id={db_task.id}")
        return db_task

    async def get(self, task_id: UUID) -> Optional[Task]:
        logger.debug(f"Fetching task with id={task_id}")
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        task = result.scalar_one_or_none()
        if task:
            logger.info(f"Task fetched with id={task_id}")
        else:
            logger.warning(f"Task with id={task_id} not found")
        return task

    async def get_list(self, skip: int = 0, limit: int = 100) -> List[Task]:
        logger.debug(f"Fetching tasks with skip={skip}, limit={limit}")
        query = select(Task).offset(skip).limit(limit)
        result = await self.db.execute(query)
        tasks = result.scalars().all()
        logger.info(f"Fetched {len(tasks)} tasks")
        return tasks

    async def update(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        logger.debug(f"Updating task with id={task_id}")
        query = update(Task).where(Task.id == task_id).values(**task_update.model_dump(exclude_unset=True))
        result = await self.db.execute(query)
        if result.rowcount == 0:
            logger.warning(f"Task with id={task_id} not found for update")
            return None
        await self.db.commit()
        task = await self.get(task_id)
        logger.info(f"Task updated with id={task_id}")
        return task

    async def delete(self, task_id: UUID) -> bool:
        logger.debug(f"Deleting task with id={task_id}")
        query = delete(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        await self.db.commit()
        if result.rowcount == 0:
            logger.warning(f"Task with id={task_id} not found for deletion")
            return False
        logger.info(f"Task deleted with id={task_id}")
        return True
