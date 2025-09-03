import uuid
import pytest
import logging
from fastapi import FastAPI
from src.main import lifespan
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.schemas.task import TaskCreate, TaskUpdate
from src.services.task import TaskService
from uuid import UUID

logger = logging.getLogger("src.test")


class TestTasksAPI:
    @pytest.mark.asyncio
    async def test_create_task(self, client):
        logger.info("Starting test_create_task")
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "status": "created",
        }
        response = await client.post("/api/v1/tasks/", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert UUID(data["id"])
        logger.info("test_create_task passed")

    @pytest.mark.asyncio
    async def test_get_task(self, client, task_service: TaskService):
        logger.info("Starting test_get_task")
        task_data = TaskCreate(title="Test Task", description="Test Description", status="created")
        created_task = await task_service.create_task(task_data)
        response = await client.get(f"/api/v1/tasks/{created_task.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(created_task.id)
        assert data["title"] == task_data.title
        assert data["description"] == task_data.description
        assert data["status"] == task_data.status
        logger.info("test_get_task passed")

    @pytest.mark.asyncio
    async def test_get_tasks(self, client, task_service: TaskService):
        logger.info("Starting test_get_tasks")
        task_data = TaskCreate(title="Test Task", description="Test Description", status="created")
        await task_service.create_task(task_data)
        response = await client.get("/api/v1/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["title"] == task_data.title
        logger.info("test_get_tasks passed")

    @pytest.mark.asyncio
    async def test_update_task(self, client, task_service: TaskService):
        logger.info("Starting test_update_task")
        task_data = TaskCreate(title="Test Task", description="Test Description", status="created")
        created_task = await task_service.create_task(task_data)
        update_data = {"title": "Updated Task", "status": "in_progress"}
        response = await client.put(f"/api/v1/tasks/{created_task.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
        logger.info("test_update_task passed")

    @pytest.mark.asyncio
    async def test_delete_task(self, client, task_service: TaskService):
        logger.info("Starting test_delete_task")
        task_data = TaskCreate(title="Test Task", description="Test Description", status="created")
        created_task = await task_service.create_task(task_data)
        response = await client.delete(f"/api/v1/tasks/{created_task.id}")

        assert response.status_code == 204
        response = await client.get(f"/api/v1/tasks/{created_task.id}")
        assert response.status_code == 404
        logger.info("test_delete_task passed")

    @pytest.mark.asyncio
    @staticmethod
    async def test_app_lifespan_shutdown():
        app = FastAPI(lifespan=lifespan)
        async with app.router.lifespan_context(app):
            assert hasattr(app.state, "db_pool")

    @pytest.mark.asyncio
    async def test_update_nonexistent_task(self, task_service: TaskService):
        fake_id = uuid.uuid4()
        with pytest.raises(HTTPException):
            await task_service.update_task(fake_id, TaskUpdate(title="No Task"))

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task(self, task_service: TaskService):
        fake_id = uuid.uuid4()
        with pytest.raises(HTTPException):
            await task_service.delete_task(fake_id)

    @pytest.mark.asyncio
    async def test_create_task_without_title(self, task_service: TaskService):
        with pytest.raises(HTTPException):
            await task_service.create_task(TaskCreate(title="", description="No title"))

    @pytest.mark.asyncio
    async def test_update_task_without_status(self, task_service: TaskService):
        task_data = TaskCreate(title="Task", description="desc")
        created_task = await task_service.create_task(task_data)

        with pytest.raises(IntegrityError):
            await task_service.repository.update(
                created_task.id,
                TaskUpdate(title="Updated Task", status=None)
            )
