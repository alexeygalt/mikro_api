from dataclasses import dataclass

from exeptions import TaskNotFoundException
from repository.cache_task import TaskCache
from repository.task import TaskRepository
from schema.tasks import TaskSchema, TaskBaseSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks

        tasks = self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(tasks_schema)
        return tasks

    def create_task(self, task: TaskBaseSchema, user_id: int) -> TaskSchema:
        task = self.task_repository.create_task(task, user_id)
        return task

    def get_task(self, task_id: int, user_id: int) -> TaskSchema:
        task = self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFoundException
        return task

    def update_task(self, task_id: int, task: TaskBaseSchema) -> TaskSchema:
        return self.task_repository.update_task(task_id, task)

    def delete_task(self, task_id: int):
        self.task_repository.delete_task(task_id)