from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session as OrmSession

from app.core.database import get_db
from app.repositories.job import JobRepository
from app.repositories.message import MessageRepository
from app.repositories.session import SessionRepository
from app.services.agent.async_processing_service import (
    AsyncProcessingService,
)
from app.services.domain.message_service import (
    MessageService,
    MessageTransformer,
)
from app.services.domain.session_service import (
    SessionService,
    AutoTitleGenerator,
)
from app.services.seo_agent_service import SEOAgentService


# Repository Dependencies
def get_session_repository(db: OrmSession = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db)


def get_message_repository(db: OrmSession = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)


def get_job_repository(db: OrmSession = Depends(get_db)) -> JobRepository:
    return JobRepository(db)


# Service Dependencies
@lru_cache()
def get_title_generator() -> AutoTitleGenerator:
    return AutoTitleGenerator()


@lru_cache()
def get_message_transformer() -> MessageTransformer:
    return MessageTransformer()


def get_session_service(
    session_repo: SessionRepository = Depends(get_session_repository),
    title_generator: AutoTitleGenerator = Depends(get_title_generator),
) -> SessionService:
    return SessionService(session_repo, title_generator)


def get_message_service(
    message_repo: MessageRepository = Depends(get_message_repository),
    transformer: MessageTransformer = Depends(get_message_transformer),
) -> MessageService:
    return MessageService(message_repo, transformer)


def get_async_processing_service(
    job_repo: JobRepository = Depends(get_job_repository),
) -> AsyncProcessingService:
    return AsyncProcessingService(job_repo)


def get_seo_agent_service(
    message_service: MessageService = Depends(get_message_service),
) -> SEOAgentService:
    return SEOAgentService(message_service)
