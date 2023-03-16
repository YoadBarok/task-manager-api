from sqlalchemy.orm import Session, joinedload
from src.app.schemas.task import JobState
from src.app.models.task import Task
from src.app.schemas.task import Task as TaskSchema
from src.app.utils.task_utils import convert_job_state, process_task
import uuid
import asyncio


def find_all_tasks(db: Session):
    all_tasks = db.query(Task).options(joinedload(Task.owner)).all()
    result = [convert_job_state(task) for task in all_tasks]
    return result


def find_task_by_id(db: Session, task_id: int):
    _task = db.query(Task).filter(Task.id == task_id).first()
    if _task is None:
        return None
    _task.job_state = JobState(_task.job_state).name
    return _task


def create_task(db: Session, task: TaskSchema):
    _task = Task(
        name=task.name,
        job_id=str(uuid.uuid4()),
        job_state=JobState.WORKING.value,
        owner_id=task.owner_id
    )
    db.add(_task)
    db.commit()
    db.refresh(_task)
    asyncio.create_task(process_task(_task.job_id, db))
    _task = convert_job_state(_task)
    return _task


def edit_task(db: Session, task_id: int, task: TaskSchema):
    _task = db.query(Task).filter(Task.id == task_id).first()
    if _task is None:
        return None
    _task.name = task.name
    _task.owner_id = task.owner_id
    db.commit()
    db.refresh(_task)
    return _task


def remove_task(db: Session, task_id: int):
    _task = db.query(Task).filter(Task.id == task_id).first()
    if _task is None:
        return None
    db.delete(_task)
    db.commit()
    return _task


