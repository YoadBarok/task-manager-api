from sqlalchemy.orm import Session
from src.app.models.user import User


def seed_db(db: Session):
    users = db.query(User).all()
    if len(users) == 0:
        first_user = User(name="First User")
        second_user = User(name="Second User")
        db.add(first_user)
        db.add(second_user)
        db.commit()
