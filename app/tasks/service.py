from dataclasses import dataclass
from app.exeptions import TaskNotFoundException
from app.tasks.repository.cache_task import TaskCache
from app.tasks.repository.task import TaskRepository
from app.tasks.schema import TaskSchema, TaskBaseSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[TaskSchema]:
        if tasks := await self.task_cache.get_tasks():
            return tasks

        tasks = await self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        await self.task_cache.set_tasks(tasks_schema)
        return tasks

    async def create_task(self, task: TaskBaseSchema, user_id: int) -> TaskSchema:
        task = await self.task_repository.create_task(task, user_id)
        return task

    async def get_task(self, task_id: int, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_task(
            task_id=task_id, user_id=user_id
        )
        if not task:
            raise TaskNotFoundException
        return task

    async def update_task(self, task_id: int, task: TaskBaseSchema) -> TaskSchema:
        return await self.task_repository.update_task(task_id, task)

    async def delete_task(self, task_id: int):
        await self.task_repository.delete_task(task_id)
