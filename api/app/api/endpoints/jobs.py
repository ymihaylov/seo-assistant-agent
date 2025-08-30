from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as OrmSession

from app.core.auth import verify_jwt
from app.core.database import get_db
from app.enums import JobStatus
from app.models.message import Message
from app.schemas.job import JobStatusResponse
from app.schemas.message import MessageOut
from app.services.domain.job_service import get_job_with_messages
from app.services.domain.user_service import UserService

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _to_message_out(m: Message) -> MessageOut:
    return MessageOut(
        id=m.id,
        role=m.role,
        message_content=m.message_content,
        suggested_page_title=m.suggested_page_title,
        suggested_page_content=m.suggested_page_content,
        suggested_title_tag=m.suggested_title_tag,
        suggested_meta_description=m.suggested_meta_description,
        suggested_meta_keywords=m.suggested_meta_keywords,
        created_at=m.created_at.isoformat() if m.created_at else "",
        updated_at=m.updated_at.isoformat() if m.updated_at else "",
    )


@router.get("/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
):
    job = get_job_with_messages(db, job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    user_service = UserService(db)

    # ENSURE USER
    user = user_service.ensure_user(claims)
    # Verify job belongs to the authenticated user
    if job.user_id != user.id:  # Adjust based on your JWT structure
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    # Get agent message if job is completed
    agent_message = None
    if job.status == JobStatus.COMPLETED and job.agent_message_id:
        agent_msg = db.query(Message).filter(Message.id == job.agent_message_id).first()
        if agent_msg:
            agent_message = _to_message_out(agent_msg)

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        agent_message=agent_message,
        processing_time_seconds=job.processing_time_seconds,
        error_message=job.error_message,
        updated_at=job.updated_at.isoformat() if job.updated_at else "",
    )
