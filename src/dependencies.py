from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.services.task import TaskService
from fastapi import Depends


async def get_task_service(db: AsyncSession = Depends(get_db)):
    return TaskService(db)
