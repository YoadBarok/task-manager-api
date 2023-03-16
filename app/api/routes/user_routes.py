from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.user import RequestUser
from schemas.response import Response
from api.controllers import user_controller

router = APIRouter()

@router.get('/')
async def all_users(db: Session=Depends(get_db)):
    _users = user_controller.get_all_users(db)
    return Response(code=200, status="Ok", message="Users fetched", result=_users)


@router.post('/create-user')
async def create_user(request: RequestUser, db: Session=Depends(get_db)):
    _user = user_controller.create_user(request, db)
    return Response(code=201, status="Ok", message="Users created", result=_user)


@router.delete('/delete-user/{id}')
async def remove_user(id: int, db: Session=Depends(get_db)):
    _user = user_controller.remove_user(db, id)
    return Response(code=204, status="Ok", message="User deleted", result=_user)