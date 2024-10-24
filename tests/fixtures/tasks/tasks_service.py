import pytest

from app.tasks.service import TaskService


@pytest.fixture
def tasks_service(tasks_repository, get_task_cache_repository):
    return TaskService(task_cache=get_task_cache_repository,
                       task_repository=tasks_repository)
