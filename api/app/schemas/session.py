from typing import Optional

from pydantic import BaseModel, Field

from app.enums import JobStatus
from app.schemas.message import MessageOut


class SessionCreateRequest(BaseModel):
    message: str = Field(..., min_length=1)
    title: Optional[str] = None


class SessionCreateResponse(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    session_title: str
    message: MessageOut


class SessionStartResponse(BaseModel):
    session_id: str
    user_id: str
    session_title: str
    user_message: MessageOut
    agent_message: MessageOut


class AsyncSessionStartResponse(BaseModel):
    session_id: str
    session_title: str
    job_id: str
    user_message: MessageOut
    status: JobStatus


class SessionListResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    last_message_at: str

    class Config:
        from_attributes = True


class SessionUpdateRequest(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="New session title"
    )


class SessionUpdateResponse(BaseModel):
    id: str
    title: str
    updated_at: str

    class Config:
        from_attributes = True
