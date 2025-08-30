from typing import Optional

from pydantic import BaseModel

from app.enums import JobStatus
from app.schemas.message import MessageOut


class JobResponse(BaseModel):
    job_id: str
    user_message: MessageOut
    status: JobStatus
    processing_time_seconds: Optional[float] = None
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None
    created_at: str
    updated_at: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    agent_message: Optional[MessageOut] = None
    processing_time_seconds: Optional[float] = None
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None
    updated_at: str
