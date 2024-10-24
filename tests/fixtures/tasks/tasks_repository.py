import pytest

from app.tasks.repository.task import TaskRepository


@pytest.fixture
def tasks_repository(get_db_session):
    return TaskRepository(db_session=get_db_session)