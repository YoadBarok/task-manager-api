from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.app.api.repositories import task_repository
from src.app.schemas.response import Response
from src.app.schemas.task import RequestTask
from src.app.api.repositories import user_repository


def get_all_tasks(db: Session):
    try:
        _tasks = task_repository.find_all_tasks(db)
        return Response(code=200, status="Ok", message="Tasks fetched", result=_tasks)
    except Exception:
        return HTTPException(status_code=500, detail="Fetching tasks failed")


def get_all_completed_tasks(db: Session):
    try:
        _tasks = task_repository.find_all_completed_tasks(db)
        return Response(code=200, status="Ok", message="Tasks fetched", result=_tasks)
    except Exception:
        return HTTPException(status_code=500, detail="Fetching tasks failed")


def create_task(request: RequestTask, db: Session):
    _user = user_repository.find_user_by_id(db, request.task.owner_id)
    if not _user:
        raise HTTPException(status_code=400, detail="Cannot find a user with the provided owner_id")
    _task = task_repository.create_task(db, request.task)
    return Response(code=201, status="Ok", message="Task created successfully", result=_task)


def get_task_by_id(task_id: int, db: Session):
    _task = task_repository.find_task_by_id(db, task_id)
    if not _task:
        raise HTTPException(status_code=404, detail="Task not found")
    return _task


def edit_task(task_id: int, db: Session, request: RequestTask):
    _task = task_repository.edit_task(db, task_id, request.task)
    if not _task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(code=200, status="Ok", message="Task updated successfully", result=_task)


def remove_task(task_id: int, db: Session):
    _task = task_repository.remove_task(db, task_id)
    if not _task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(code=204, status="Deleted", message="Task deleted successfully", result=_task)
