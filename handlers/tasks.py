from fastapi import HTTPException, status, Response
from typing import Annotated
from fastapi import APIRouter, Depends

from repository.cache_task import TaskCache
from schema.tasks import TaskSchema, TaskBaseSchema
from repository.task import TaskRepository
from dependency import get_tasks_repository, get_task_cache_repository
from service.task import TaskService

router = APIRouter(prefix="/task", tags=['task'])

router.get('/')


@router.get('/all', response_model=list[TaskSchema])
# async def get_task(task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
#                    task_cache: Annotated[TaskCache, Depends(get_task_cache_repository)]):
#     if tasks := task_cache.get_tasks():
#         return tasks
#
#     tasks = task_repository.get_tasks()
#     tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
#     task_cache.set_tasks(tasks_schema)
#     return tasks
async def get_task(task_service: Annotated[TaskService, Depends(get_tasks_repository)]):
    return task_service.get_tasks()


@router.post('/', response_model=TaskSchema)
async def create_task(task: TaskBaseSchema, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task = task_repository.create_task(task)
    return task


@router.patch('/{task_id}', response_model=TaskSchema)
async def update_task(task: TaskBaseSchema, task_id: int,
                      task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    if not task_repository.get_task(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task = task_repository.update_task(task_id, task)

    return task


@router.delete('/{task_id}')
async def delete_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    if not task_repository.get_task(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_repository.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
