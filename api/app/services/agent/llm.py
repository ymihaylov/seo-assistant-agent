import json

from openai import AsyncOpenAI

from app.core.settings import get_settings

s = get_settings()
_client = AsyncOpenAI(api_key=s.openai_api_key)


async def chat_json(system: str, user: str) -> dict:
    resp = await _client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    return json.loads(resp.choices[0].message.content)
