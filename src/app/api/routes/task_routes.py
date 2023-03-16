from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.app.api.deps import get_db
from src.app.schemas.task import RequestTask
from src.app.schemas.response import Response
from src.app.api.controllers import task_controller


router = APIRouter()


@router.get('/')
async def all_tasks(db: Session = Depends(get_db)):
    return task_controller.get_all_tasks(db)


@router.get('/{id}')
async def get_task_by_id(id: int, db: Session = Depends(get_db)):
    _task = task_controller.get_task_by_id(id, db)
    return Response(code=200, status="Ok", message="Task found", result=_task)


@router.post('/create-task')
async def create_task(request: RequestTask, db: Session = Depends(get_db)):
    return task_controller.create_task(request, db)


@router.post('/edit/{id}')
async def edit_task(request: RequestTask, id: int, db: Session = Depends(get_db)):
    return task_controller.edit_task(id, db, request)


@router.delete('/delete/{id}')
async def delete_task(id: int, db: Session = Depends(get_db)):
    return task_controller.remove_task(id, db)
