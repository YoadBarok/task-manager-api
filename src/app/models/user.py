from typing import List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.app.db.base_class import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )