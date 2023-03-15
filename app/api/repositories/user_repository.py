from sqlalchemy.orm import Session
from models.user import User
from schemas.user import User as UserSchema


def find_all_users(db: Session):
    all_users = db.query(User).all()
    return all_users


def find_user_by_id(db: Session, user_id):
    _user = db.query(User).filter(User.id == user_id).first()
    if not _user:
        return None
    return _user


def create_user(db: Session, user: UserSchema):
    _user = User(name=user.name)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def remove_user(db: Session, user_id: int):
    _user = find_user_by_id(db, user_id)
    db.delete(_user)
    db.commit()
    return _user
