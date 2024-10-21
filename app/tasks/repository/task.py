from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Tasks, Categories
from app.tasks.schema import TaskBaseSchema, TaskSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int):
        query = select(Tasks).where(Tasks.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    # def get_tasks(self) -> list[TaskSchema]:
    async def get_tasks(self) -> list[Tasks]:
        async with self.db_session as session:
            tasks = (await session.execute(select(Tasks))).scalars().all()
        return tasks

    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskBaseSchema, user_id: int) -> TaskSchema:
        task = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id, user_id=user_id)
        async with self.db_session as session:
            session.add(task)
            await session.commit()
            await session.refresh(task)
        return task

    async def update_task(self, task_id: int, task: TaskBaseSchema):
        async with self.db_session as session:
            query = update(Tasks).where(Tasks.id == task_id).values(**task.dict(exclude_none=True))
            await session.execute(query)
            await session.commit()

        return await self.get_task(task_id)

    async def delete_task(self, task_id: int) -> None:
        async with self.db_session as session:
            query = delete(Tasks).where(Tasks.id == task_id)
            await session.execute(query)
            await session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(
            Categories.name == category_name)
        async with self.db_session as session:
            tasks = (await session.execute(query)).scalars().all()
        return tasks
