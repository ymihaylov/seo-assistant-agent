from typing import List

from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException, Query
from sqlalchemy.orm import Session as OrmSession

from app.core.auth import verify_jwt
from app.core.database import get_db
from app.dependencies import (
    get_session_service,
    get_message_service,
    get_async_processing_service,
    get_seo_agent_service,
)
from app.schemas.message import MessageCreateRequest, MessageOut, AsyncMessageResponse
from app.schemas.session import (
    SessionCreateRequest,
    SessionStartResponse,
    AsyncSessionStartResponse,
    SessionListResponse,
    SessionUpdateRequest,
    SessionUpdateResponse,
)
from app.services.agent.async_processing_service import AsyncProcessingService
from app.services.domain.job_service import process_agent_job
from app.services.domain.message_service import MessageService
from app.services.domain.session_service import SessionService
from app.services.domain.user_service import UserService
from app.services.seo_agent_service import SEOAgentService

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post(
    "/async",
    response_model=AsyncSessionStartResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_session_async(
    payload: SessionCreateRequest,
    background_tasks: BackgroundTasks,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    session_service: SessionService = Depends(get_session_service),
    message_service: MessageService = Depends(get_message_service),
    async_service: AsyncProcessingService = Depends(get_async_processing_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    session = session_service.create_session(user.id, payload.title, payload.message)
    user_message = message_service.create_user_message(session.id, payload.message)

    job = async_service.create_processing_job(user.id, session.id, user_message)

    db.commit()

    background_tasks.add_task(process_agent_job, job.id)

    db.refresh(user_message)
    db.refresh(session)

    return async_service.build_session_start_response(
        session.id, session.title, job, user_message
    )


@router.post(
    "", response_model=SessionStartResponse, status_code=status.HTTP_201_CREATED
)
async def create_session(
    payload: SessionCreateRequest,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    session_service: SessionService = Depends(get_session_service),
    message_service: MessageService = Depends(get_message_service),
    ai_service: SEOAgentService = Depends(get_seo_agent_service),
):
    """Create a session with synchronous agent processing."""
    user_service = UserService(db)
    user = user_service.ensure_user(claims)
    session = session_service.create_session(user.id, payload.title, payload.message)
    user_message = message_service.create_user_message(session.id, payload.message)
    db.flush()

    suggestions = await ai_service.process_first_message_new_session(
        session.title, payload.message
    )

    agent_message = message_service.create_agent_message(session.id, suggestions)

    db.commit()

    db.refresh(user_message)
    db.refresh(session)

    return SessionStartResponse(
        session_id=session.id,
        user_id=user.id,
        session_title=session.title,
        user_message=message_service._transformer.to_message_out(user_message),
        agent_message=agent_message,
    )


@router.post(
    "/{session_id}/messages/async",
    response_model=AsyncMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_message_to_session_async(
    session_id: str,
    payload: MessageCreateRequest,
    background_tasks: BackgroundTasks,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    session_service: SessionService = Depends(get_session_service),
    message_service: MessageService = Depends(get_message_service),
    async_service: AsyncProcessingService = Depends(get_async_processing_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    session = session_service.get_session(session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_message = message_service.create_user_message(session_id, payload.message)

    job = async_service.create_processing_job(user.id, session_id, user_message)

    db.commit()

    background_tasks.add_task(process_agent_job, job.id)

    db.refresh(user_message)

    return async_service.build_message_response(session_id, job, user_message)


@router.post(
    "/{session_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_message_to_session(
    session_id: str,
    payload: MessageCreateRequest,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    session_service: SessionService = Depends(get_session_service),
    message_service: MessageService = Depends(get_message_service),
    ai_service: SEOAgentService = Depends(get_seo_agent_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    session = session_service.get_session(session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_message = message_service.create_user_message(session_id, payload.message)
    db.flush()

    suggestions = await ai_service.process_message_to_existing_session(
        session_id, session.title, user_message.message_content
    )

    agent_message = message_service.create_agent_message(session_id, suggestions)

    db.commit()

    return agent_message


@router.get("", response_model=List[SessionListResponse])
async def get_user_sessions(
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    limit: int = Query(default=50, le=100, description="Max sessions to return"),
    offset: int = Query(default=0, ge=0, description="Number of sessions to skip"),
    session_service: SessionService = Depends(get_session_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    return session_service.get_user_sessions(user.id, limit, offset)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    session_service: SessionService = Depends(get_session_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    success = session_service.delete_session(session_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")


@router.patch("/{session_id}", response_model=SessionUpdateResponse)
async def update_session(
    session_id: str,
    payload: SessionUpdateRequest,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    session_service: SessionService = Depends(get_session_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    result = session_service.update_session(session_id, user.id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")

    return result


@router.get("/{session_id}/messages", response_model=List[MessageOut])
async def get_session_messages(
    session_id: str,
    db: OrmSession = Depends(get_db),
    claims: dict = Depends(verify_jwt),
    limit: int = Query(default=100, le=500, description="Max messages to return"),
    offset: int = Query(default=0, ge=0, description="Number of messages to skip"),
    session_service: SessionService = Depends(get_session_service),
    message_service: MessageService = Depends(get_message_service),
):
    user_service = UserService(db)
    user = user_service.ensure_user(claims)

    session = session_service.get_session(session_id, user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return message_service.get_session_messages(session_id, limit, offset)
