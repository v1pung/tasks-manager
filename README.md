## Task Manager API

FastAPI-приложение для управления задачами с использованием слоистой архитектуры 
и паттерна репозиторий. Реализованы CRUD-операции над задачами 
со статусами (`created`, `in_progress`, `completed`).

### Возможности
- Создание, получение, обновление и удаление задач  
- Модель задачи: `UUID`, заголовок, описание, статус  
- Разделение на уровни: API → сервисы → репозитории → БД  
- PostgreSQL в Docker Compose  
- Конфигурация через `.env` и Pydantic  
- Автоматическая документация Swagger по адресу `/docs`  
- Покрытие тестами (pytest + coverage: 91%) 

### Требования
- Python 3.12+
- Poetry
- Docker и Docker Compose

Стек: Python, FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Asyncpg, Pytest.

### Установка и запуск

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/v1pung/tasks-manager.git
   cd tasks-manager
   ```

2. **Установить зависимости**:
   ```bash
   poetry install
   ```

3. **Создать файл окружения**:
   Скопировать пример и при необходимости отредактировать значения:
   ```bash
   mv .env-example .env
   ```

4. **Локальный запуск**:
   ```bash
   docker-compose up -d db
   poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Доступ к API**:
   - Swagger UI: `http://localhost:8000/docs`
   - API endpoint: `http://localhost:8000`
   

6. **Запуск в контейнере**:
   ```bash
   docker compose up -d
   ```

## Структура проекта
```
tasks-manager/
├── src/
│   ├── api/                # Маршруты и обработчики API
│   ├── core/               # Конфигурация и настройки
│   ├── db/                 # Сессии и инициализация БД
│   ├── models/             # SQLAlchemy-модели
│   ├── schemas/            # Pydantic-схемы
│   ├── services/           # Бизнес-логика
│   ├── repositories/       # Доступ к данным
│   ├── main.py             # Точка входа FastAPI-приложения
│   └── dependencies.py     # Зависимости для DI
├── tests/                  # Тесты (pytest)
├── docker-compose.yml      # Конфигурация сервисов
├── Dockerfile              # Образ приложения
├── pyproject.toml          # Зависимости Poetry
├── poetry.lock             # Зафиксированные версии зависимостей
├── .env-example            # Пример переменных окружения
└── README.md               # Документация
```

## Тестирование
Проект содержит полноценный набор тестов на базе **pytest**, который покрывает:  
- эндпоинты API  
- бизнес-логику сервисного слоя  
- взаимодействие с репозиториями  
- граничные случаи и обработку ошибок
Для тестов используется схема test в существующей БД.

Запуск тестов:  
   ```bash
   poetry run pytest --cov -v
   ```

