import json
import httpx
from app.core.config import settings

class QwenClient:
    def __init__(self):
        self.api_key = settings.qwen_api_key
        self.base_url = settings.qwen_base_url.rstrip("/")
        self.model = settings.qwen_model

    async def json_chat(self, system: str, user: str, fallback: dict) -> dict:
        if not self.api_key:
            return fallback
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user},
                        ],
                        "temperature": 0.2,
                        "response_format": {"type": "json_object"},
                    },
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
                return json.loads(content)
        except Exception as exc:
            fallback["qwen_error"] = str(exc)
            fallback["used_fallback"] = True
            return fallback

qwen_client = QwenClient()
