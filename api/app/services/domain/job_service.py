from typing import Optional

from sqlalchemy.orm import Session as OrmSession

from app.core.database import get_db
from app.models.job import Job
from app.services.agent.job_pipeline import JobPipeline


async def process_agent_job(job_id: str) -> None:
    with next(get_db()) as db_session:
        pipeline = JobPipeline()
        await pipeline.process(job_id, db_session)


def get_job_with_messages(db: OrmSession, job_id: str) -> Optional[Job]:
    return db.query(Job).filter(Job.id == job_id).first()
