import time
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session as OrmSession

from app.models.job import Job, JobStatus
from app.models.message import Message
from app.models.session import Session as SessionModel
from app.repositories.message import MessageRepository
from app.services.domain.message_service import MessageService, MessageTransformer
from app.services.seo_agent_service import SEOAgentService


@dataclass
class JobContext:
    job: Job
    session: SessionModel
    user_message: Message
    db_session: OrmSession
    start_time: float
    ai_service: Optional[SEOAgentService] = None
    suggestions: Optional[dict] = None
    agent_message: Optional[Message] = None


class JobPipeline:
    async def process(self, job_id: str, db_session: OrmSession) -> None:
        context = JobContext(
            job=None,
            session=None,
            user_message=None,
            db_session=db_session,
            start_time=time.time(),
        )

        try:
            await self._load_job_data(job_id, context)
            await self._validate_data(context)
            await self._initialize_services(context)
            await self._generate_suggestions(context)
            await self._create_agent_message(context)
            await self._complete_job(context)

        except Exception as e:
            await self._handle_error(context, e)

    async def _load_job_data(self, job_id: str, context: JobContext) -> None:
        context.job = context.db_session.query(Job).filter(Job.id == job_id).first()
        if not context.job:
            raise ValueError("Job not found")

        context.job.status = JobStatus.GENERATING
        context.db_session.commit()

        context.session = (
            context.db_session.query(SessionModel)
            .filter(SessionModel.id == context.job.session_id)
            .first()
        )
        context.user_message = (
            context.db_session.query(Message)
            .filter(Message.id == context.job.user_message_id)
            .first()
        )

    async def _validate_data(self, context: JobContext) -> None:
        if not context.session or not context.user_message:
            raise ValueError("Session or user message not found")

    async def _initialize_services(self, context: JobContext) -> None:
        message_repo = MessageRepository(context.db_session)
        message_transformer = MessageTransformer()
        message_service = MessageService(message_repo, message_transformer)
        context.ai_service = SEOAgentService(message_service)

    async def _generate_suggestions(self, context: JobContext) -> None:
        first_message = context.ai_service._message_service.get_first_message(
            context.job.session_id
        )
        is_first_message = (
            first_message is None or first_message.id == context.user_message.id
        )

        if is_first_message:
            context.suggestions = (
                await context.ai_service.process_first_message_new_session(
                    context.session.title, context.user_message.message_content
                )
            )
        else:
            context.suggestions = (
                await context.ai_service.process_message_to_existing_session(
                    context.job.session_id,
                    context.session.title,
                    context.user_message.message_content,
                )
            )

    async def _create_agent_message(self, context: JobContext) -> None:
        suggestions = self._normalize_suggestions(context.suggestions)

        context.agent_message = Message(
            session_id=context.job.session_id,
            role="agent",
            message_content="",
            suggested_page_title=suggestions["page_title"],
            suggested_page_content=suggestions["page_content"],
            suggested_title_tag=suggestions["title_tag"],
            suggested_meta_description=suggestions["meta_description"],
            suggested_meta_keywords=suggestions["meta_keywords"],
        )

        context.db_session.add(context.agent_message)
        context.db_session.flush()

    async def _complete_job(self, context: JobContext) -> None:
        processing_time = time.time() - context.start_time
        context.job.agent_message_id = context.agent_message.id
        context.job.status = JobStatus.COMPLETED
        context.job.processing_time_seconds = processing_time
        context.db_session.commit()

    async def _handle_error(self, context: JobContext, error: Exception) -> None:
        processing_time = time.time() - context.start_time

        if context.job:
            context.job.status = JobStatus.FAILED
            context.job.error_message = str(error)[:500]
            context.job.processing_time_seconds = processing_time
            context.db_session.commit()

    def _normalize_suggestions(self, suggestions: dict) -> dict:
        return {
            "page_title": (suggestions.get("page_title") or None),
            "page_content": (suggestions.get("page_content") or ""),
            "title_tag": (suggestions.get("title_tag") or None),
            "meta_description": (suggestions.get("meta_description") or None),
            "meta_keywords": list(suggestions.get("meta_keywords") or []),
        }
