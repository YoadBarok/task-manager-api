from sqlalchemy.orm import Session
from src.app.api.repositories import user_repository
from src.app.schemas.user import RequestUser


def get_all_users(db: Session):
    return user_repository.find_all_users(db)


def create_user(request: RequestUser, db: Session):
    return user_repository.create_user(db, request.user)


def remove_user(db: Session, user_id: int):
    return user_repository.remove_user(db, user_id)