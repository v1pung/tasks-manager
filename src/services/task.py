import logging
from src.repositories.task import TaskRepository
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from fastapi import HTTPException

logger = logging.getLogger("src")


class TaskService:
    def __init__(self, db: AsyncSession):
        self.repository = TaskRepository(db)

    async def create_task(self, task: TaskCreate) -> TaskResponse:
        if not task.title:
            logger.error("Attempted to create task with empty title")
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        db_task = await self.repository.create(task)
        logger.info(f"Created task with id={db_task.id}")
        return TaskResponse.model_validate(db_task)

    async def get_task(self, task_id: UUID) -> Optional[TaskResponse]:
        db_task = await self.repository.get(task_id)
        if not db_task:
            logger.warning(f"Task with id={task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info(f"Retrieved task with id={task_id}")
        return TaskResponse.model_validate(db_task)

    async def get_tasks(self, skip: int = 0, limit: int = 100) -> List[TaskResponse]:
        tasks = await self.repository.get_list(skip, limit)
        logger.info(f"Retrieved {len(tasks)} tasks with skip={skip}, limit={limit}")
        return [TaskResponse.model_validate(task) for task in tasks]

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Optional[TaskResponse]:
        db_task = await self.repository.update(task_id, task_update)
        if not db_task:
            logger.warning(f"Task with id={task_id} not found for update")
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info(f"Updated task with id={task_id}")
        return TaskResponse.model_validate(db_task)

    async def delete_task(self, task_id: UUID) -> None:
        if not await self.repository.delete(task_id):
            logger.warning(f"Task with id={task_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info(f"Deleted task with id={task_id}")
