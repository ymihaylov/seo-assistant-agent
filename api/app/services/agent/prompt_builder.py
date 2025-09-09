from typing import Dict, Any


class SEOPromptBuilder:
    def build_user_payload(self, state: Dict[str, Any]) -> str:
        """
        Build prompt from state context.
        Expected state:
          session_title: str
          instructions: str (current user message)
          anchor: str | None (first user message)
          current_draft: dict | None (previous agent suggestions)
          constraints: dict | None (SEO constraints)
        """
        parts = [
            f'Session Title: "{state.get("session_title", "")}"',
        ]

        constraints = state.get("constraints", {})
        if constraints:
            constraint_text = []
            if "title_max" in constraints:
                constraint_text.append(
                    f"Title max length: {constraints['title_max']} chars"
                )
            if (
                "meta_description_min" in constraints
                and "meta_description_max" in constraints
            ):
                constraint_text.append(
                    f"Meta description: {constraints['meta_description_min']}-{constraints['meta_description_max']} chars"
                )
            if constraint_text:
                parts.append("Constraints: " + ", ".join(constraint_text))

        anchor = (state.get("anchor") or "").strip()
        if anchor:
            parts.append(f'Original Request: """{anchor}"""')

        current_draft = state.get("current_draft")
        if current_draft:
            draft_parts = []
            for key, value in current_draft.items():
                if value:
                    if key == "meta_keywords" and isinstance(value, list):
                        draft_parts.append(f"{key}: {', '.join(value)}")
                    else:
                        draft_parts.append(f"{key}: {value}")
            if draft_parts:
                parts.append("Current Draft:\n" + "\n".join(draft_parts))

        instr = (state.get("instructions") or "").strip()
        if instr:
            parts.append(f'Current User Instruction: """{instr}"""')

        parts.append("Return JSON only.")
        return "\n".join(parts)
