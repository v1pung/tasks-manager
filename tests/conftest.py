import pytest
import logging
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from src.main import app
from src.dependencies import get_db, get_task_service
from src.models import Base
from src.services.task import TaskService
from src.core.config import settings
from asgi_lifespan import LifespanManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("src.test")

# Тестовая схема в той же базе
TEST_DATABASE_URL = settings.DATABASE_URL
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="function")
async def client(test_db: AsyncSession):  # 👈 завязываем на test_db
    """Создаём тестовый HTTP-клиент с lifespan и тестовой БД"""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()


async def init_test_db():
    logger.info("Initializing test schema tables")

    async with test_engine.begin() as conn:
        # Удаляем всю схему test вместе с таблицами и типами
        await conn.execute(text("DROP SCHEMA IF EXISTS test CASCADE"))

        # Создаём схему заново
        await conn.execute(text("CREATE SCHEMA test"))

        # Меняем схему у всех таблиц
        for table in Base.metadata.tables.values():
            table.schema = "test"

        # Создаём таблицы и связанные типы в схеме test
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Test schema tables initialized successfully")


@pytest.fixture(scope="function")
async def test_db():
    await init_test_db()
    async with TestAsyncSessionLocal() as session:
        # Устанавливаем search_path для сессии
        await session.execute(text("SET search_path TO test"))
        yield session
    await test_engine.dispose()


@pytest.fixture
async def task_service(test_db: AsyncSession):
    return TaskService(test_db)


@pytest.fixture
def override_task_service(task_service):
    app.dependency_overrides[get_task_service] = lambda: task_service
    yield
    app.dependency_overrides.clear()
