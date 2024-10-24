from app.exeptions import TaskNotFoundException
from app.tasks.schema import TaskBaseSchema
from app.tasks.service import TaskService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.users.user_profile.models import UserProfile
import pytest


async def test_create_task__success(tasks_service: TaskService, get_db_session: AsyncSession):
    query = insert(UserProfile).values(id=200, email="test@mail.com")

    async with get_db_session as session:
        await session.execute(query)
        await session.commit()
    body = TaskBaseSchema(name="test", pomodoro_count=10, category_id=1)
    task = await tasks_service.create_task(body, user_id=200)

    assert task.user_id == 200


async def test_get_task_success(tasks_service: TaskService, get_db_session: AsyncSession):
    task = await tasks_service.get_task(task_id=1, user_id=200)
    assert task.id == 1


async def test_get_task_failure(tasks_service: TaskService, get_db_session: AsyncSession):
    with pytest.raises(TaskNotFoundException):
        await tasks_service.get_task(task_id=1, user_id=201)


async def test_get_user_task_success(tasks_service: TaskService, get_db_session):
    tasks = await tasks_service.get_tasks()
    assert len(tasks) == 1


async def test_update_task_success(tasks_service: TaskService, get_db_session: AsyncSession):
    body = TaskBaseSchema(name="new_test_name")
    task = await tasks_service.update_task(1, body)
    assert task.name == "new_test_name"


async def test_delete_task_success(tasks_service: TaskService, get_db_session: AsyncSession):
    await tasks_service.delete_task(1)
    with pytest.raises(TaskNotFoundException):
        await tasks_service.get_task(task_id=1, user_id=200)