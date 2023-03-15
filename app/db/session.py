from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from models.task import Task
from models.user import User
from db.seed import seed_db


engine = create_engine(environ.get('DB_URI'), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

User.metadata.create_all(bind=engine)
Task.metadata.create_all(bind=engine)


# Seed the db with 2 example users.
seed_db(SessionLocal())

