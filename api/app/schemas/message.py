from typing import Optional

from pydantic import BaseModel, Field

from app.enums import JobStatus


class MessageCreateRequest(BaseModel):
    message: str = Field(..., min_length=1)


class MessageOut(BaseModel):
    id: str
    role: str

    message_content: str

    suggested_page_title: Optional[str] = None
    suggested_page_content: Optional[str] = None
    suggested_title_tag: Optional[str] = None
    suggested_meta_description: Optional[str] = None
    suggested_meta_keywords: Optional[list[str] | None] = None

    created_at: str
    updated_at: str


class AddMessageResponse(BaseModel):
    session_id: str
    user_message: MessageOut
    agent_message: MessageOut


class AsyncMessageResponse(BaseModel):
    id: str
    session_id: str
    job_id: str
    user_message: MessageOut
    status: JobStatus
