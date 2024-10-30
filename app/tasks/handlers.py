import time
from fastapi import HTTPException, status, Response, BackgroundTasks
from typing import Annotated
from fastapi import APIRouter, Depends
from app.exeptions import TaskNotFoundException
from app.dependency import get_tasks_repository, get_request_user_id, get_task_service
from app.tasks.schema import TaskSchema, TaskBaseSchema
from app.tasks.service import TaskService

router = APIRouter(prefix="/task", tags=["task"])

router.get("/")


def get_tasks_log(tasks_count: int):
    time.sleep(3.0)
    print(f"get {tasks_count} tasks")


@router.get("/all", response_model=list[TaskSchema])
async def get_task(
    task_service: Annotated[TaskService, Depends(get_tasks_repository)],
    background_tasks: BackgroundTasks,
):
    tasks = await task_service.get_tasks()
    background_tasks.add_task(get_tasks_log, tasks_count=len(tasks))
    return tasks


@router.post("/", response_model=TaskSchema)
async def create_task(
    body: TaskBaseSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    return await task_service.create_task(body, user_id)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    task: TaskBaseSchema,
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        await task_service.get_task(task_id, user_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return await task_service.update_task(task_id, task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        await task_service.get_task(task_id, user_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    await task_service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
