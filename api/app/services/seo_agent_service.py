from typing import Dict, Any

from app.services.agent.agent_graph import seo_graph
from app.services.domain.message_service import MessageService


class SEOAgentService:
    DEFAULT_CONSTRAINTS = {
        "title_max": 60,
        "meta_description_min": 150,
        "meta_description_max": 160,
    }

    def __init__(self, message_service: MessageService):
        self._message_service = message_service

    async def process_first_message_new_session(
        self, session_title: str, user_message: str
    ) -> Dict[str, Any]:
        context = {
            "session_title": session_title,
            "instructions": user_message,
            "constraints": self.DEFAULT_CONSTRAINTS,
        }

        result = await seo_graph.ainvoke(context)

        return result.get("suggestions", {})

    async def process_message_to_existing_session(
        self,
        session_id: str,
        session_title: str,
        user_message: str,
    ) -> Dict[str, Any]:
        first_user_message = self._message_service.get_first_message(session_id)
        last_agent_message = self._message_service.get_last_agent_message(session_id)

        context = {
            "session_title": session_title,
            "instructions": user_message,
            "constraints": self.DEFAULT_CONSTRAINTS,
        }

        if first_user_message and first_user_message.message_content:
            context["anchor"] = first_user_message.message_content

        if last_agent_message:
            context["current_draft"] = self._message_service.extract_suggestions(
                last_agent_message
            )

        result = await seo_graph.ainvoke(context)
        return result.get("suggestions", {})
