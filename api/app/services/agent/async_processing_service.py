from app.models.job import Job, JobStatus
from app.models.message import Message
from app.repositories.job import JobRepository
from app.schemas.message import MessageOut, AsyncMessageResponse
from app.schemas.session import AsyncSessionStartResponse


class AsyncProcessingService:
    def __init__(self, job_repo: JobRepository):
        self._job_repo = job_repo

    def create_processing_job(
        self, user_id: str, session_id: str, user_message: Message
    ) -> Job:
        return self._job_repo.create_job(user_id, session_id, user_message.id)

    def build_session_start_response(
        self, session_id: str, session_title: str, job: Job, user_message: Message
    ) -> AsyncSessionStartResponse:
        return AsyncSessionStartResponse(
            session_id=session_id,
            session_title=session_title,
            job_id=job.id,
            user_message=self._build_message_out(user_message),
            status=JobStatus.PENDING,
        )

    def build_message_response(
        self, session_id: str, job: Job, user_message: Message
    ) -> AsyncMessageResponse:
        return AsyncMessageResponse(
            id=user_message.id,
            session_id=session_id,
            job_id=job.id,
            user_message=self._build_message_out(user_message),
            status=JobStatus.PENDING,
        )

    def _build_message_out(self, message: Message) -> MessageOut:
        return MessageOut(
            id=message.id,
            role=message.role,
            message_content=message.message_content,
            created_at=message.created_at.isoformat() if message.created_at else "",
            updated_at=message.updated_at.isoformat() if message.updated_at else "",
        )
