from asyncio import sleep
from models.task import Task
from schemas.task import JobState
from sqlalchemy.orm import Session
from random import randint


def convert_job_state(task):
    task.job_state = JobState(task.job_state).name
    return task


async def process_task(job_id, db: Session):
    delay = randint(7,10)
    task = db.query(Task).filter(Task.job_id == job_id).first()
    # Simulating an asych process, in this example for a time between 7-10 seconds
    await sleep(delay)
    task.job_state = JobState.COMPLETE.value
    db.add(task)
    db.commit()
    db.refresh(task)
    
