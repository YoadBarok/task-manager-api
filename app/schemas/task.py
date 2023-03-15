from pydantic import BaseModel, Field
from enum import Enum


class Task(BaseModel):
    name: str 
    owner_id: int

class RequestTask(BaseModel):
    task: Task = Field(...)



class JobState(Enum):
    WORKING = 0
    COMPLETE = 1