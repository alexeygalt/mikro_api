from sqlalchemy import select, update

from database.accessor import Session
from models.tasks import Tasks, Categories
from schema.tasks import TaskSchema, TaskBaseSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int):
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            task = session.execute(query).scalar_one_or_none()
        return task

    # def get_tasks(self) -> list[TaskSchema]:
    def get_tasks(self) -> list[Tasks]:
        with self.db_session() as session:
            tasks = session.execute(select(Tasks)).scalars().all()
        return tasks

    def create_task(self, task: TaskBaseSchema) -> TaskSchema:
        task = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id)
        with self.db_session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task

    def update_task(self, task_id: int, task: TaskBaseSchema):
        with self.db_session() as session:
            query = update(Tasks).where(Tasks.id == task_id).values(**task.dict(exclude_none=True))
            session.execute(query)
            session.commit()

        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            session.query(Tasks).filter(Tasks.id == task_id).delete()
            session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(
            Categories.name == category_name)
        with self.db_session() as session:
            tasks = session.execute(query).scalars().all()
        return tasks
