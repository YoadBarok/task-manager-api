from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.app.api.deps import get_db
from src.app.schemas.user import RequestUser
from src.app.schemas.response import Response
from src.app.api.controllers import user_controller

router = APIRouter()

@router.get('/', status_code=200)
async def all_users(db: Session=Depends(get_db)):
    _users = user_controller.get_all_users(db)
    return Response(code=200, status="Ok", message="Users fetched", result=_users)


@router.post('/create-user', status_code=201)
async def create_user(request: RequestUser, db: Session=Depends(get_db)):
    _user = user_controller.create_user(request, db)
    return Response(code=201, status="Ok", message="Users created", result=_user)


@router.delete('/delete-user/{id}', status_code=204)
async def remove_user(id: int, db: Session=Depends(get_db)):
    _user = user_controller.remove_user(db, id)
    return Response(code=204, status="Ok", message="User deleted", result=_user)