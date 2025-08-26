import logging
from fastapi import APIRouter, Depends
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task import TaskService
from src.dependencies import get_task_service
from uuid import UUID
from typing import List

logger = logging.getLogger("src")

router = APIRouter(tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    logger.debug(f"Creating task with title={task.title}")
    return await task_service.create_task(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    logger.debug(f"Fetching task with id={task_id}")
    return await task_service.get_task(task_id)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
        skip: int = 0,
        limit: int = 100,
        task_service: TaskService = Depends(get_task_service)
):
    logger.debug(f"Fetching tasks with skip={skip}, limit={limit}")
    return await task_service.get_tasks(skip, limit)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: UUID,
        task_update: TaskUpdate,
        task_service: TaskService = Depends(get_task_service)
):
    logger.debug(f"Updating task with id={task_id}")
    return await task_service.update_task(task_id, task_update)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    logger.debug(f"Deleting task with id={task_id}")
    await task_service.delete_task(task_id)
    return None
