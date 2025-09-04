from typing import Optional

from sqlalchemy.orm import Session as OrmSession

from app.enums import JobStatus
from app.models import Job


class JobRepository:
    def __init__(self, db: OrmSession):
        self._db = db

    def create_job(self, user_id: str, session_id: str, user_message_id: str) -> Job:
        job = Job(
            user_id=user_id,
            session_id=session_id,
            user_message_id=user_message_id,
            status=JobStatus.PENDING,
        )
        self._db.add(job)
        self._db.flush()

        return job

    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        return self._db.query(Job).filter(Job.id == job_id).first()

    def update_job_status(self, job: Job, status: JobStatus, **kwargs) -> Job:
        job.status = status

        for key, value in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, value)

        self._db.commit()
        self._db.refresh(job)

        return job
