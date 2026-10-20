import json
import time
import hashlib
import logging
import asyncio
from typing import List, Dict, Any, Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
import httpx
from ..config import settings

logger = logging.getLogger("novapath.llm")

T = TypeVar("T", bound=BaseModel)

class LLMServiceError(Exception):
    """Base exception for LLM gateway failures."""
    pass

class LLMOfflineError(LLMServiceError):
    """Raised when OmniRoute or AI provider is unreachable or unconfigured."""
    pass

class LLMService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_cache_ttl_seconds: int = 3600  # 1 hour
        self.cache_hits: int = 0
        self.cache_misses: int = 0

    @property
    def fast_model(self) -> str:
        return settings.OMNIROUTE_FAST_MODEL or settings.OMNIROUTE_MODEL or "auto"

    @property
    def strong_model(self) -> str:
        return settings.OMNIROUTE_STRONG_MODEL or settings.OMNIROUTE_MODEL or "auto"

    def _generate_cache_key(self, model: str, messages: List[Dict[str, str]], temperature: float, schema_name: str = "") -> str:
        serialized = json.dumps({"m": model, "msgs": messages, "t": temperature, "s": schema_name}, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def get_from_cache(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry:
            if time.time() - entry["timestamp"] < entry["ttl"]:
                self.cache_hits += 1
                return entry["data"]
            else:
                del self._cache[key]
        self.cache_misses += 1
        return None

    def set_cache(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = {
            "data": data,
            "timestamp": time.time(),
            "ttl": ttl or self.default_cache_ttl_seconds
        }

    async def _call_api_with_retry(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        max_retries: int = 2,
        api_key: Optional[str] = None,
        timeout_override: Optional[float] = None
    ) -> str:
        effective_key = (api_key or settings.OMNIROUTE_API_KEY or "").strip()
        if not effective_key:
            raise LLMOfflineError("API key is not configured.")

        # Support both OpenRouter and standard OpenAI/OmniRoute endpoints
        is_openrouter = effective_key.startswith("sk-or-")
        if is_openrouter:
            url = f"{settings.CHATBOX_BASE_URL.rstrip('/')}/chat/completions"
            effective_model = model if (model and not model.startswith("antigravity/") and model != "auto") else (settings.CHATBOX_MODEL or "openai/gpt-4o-mini")
        else:
            url = f"{settings.OMNIROUTE_BASE_URL.rstrip('/')}/chat/completions"
            effective_model = model

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {effective_key}"
        }
        if is_openrouter:
            headers["HTTP-Referer"] = settings.FRONTEND_ORIGIN or "http://localhost:5173"
            headers["X-Title"] = "NovaPath AI Platform"

        payload = {
            "model": effective_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        last_error: Optional[Exception] = None
        timeout = float(timeout_override or settings.OMNIROUTE_TIMEOUT_SECONDS)

        for attempt in range(max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        choices = data.get("choices", [])
                        if choices:
                            content = choices[0].get("message", {}).get("content", "")
                            return content
                        raise LLMServiceError("No choices returned from OmniRoute API.")
                    elif response.status_code in [429, 500, 502, 503, 504] and attempt < max_retries:
                        backoff = (2 ** attempt) * 0.75
                        logger.warning(f"OmniRoute HTTP {response.status_code}. Retrying in {backoff:.1f}s...")
                        await asyncio.sleep(backoff)
                        continue
                    else:
                        raise LLMServiceError(f"OmniRoute responded with HTTP {response.status_code}: {response.text}")
            except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = exc
                if attempt < max_retries:
                    backoff = (2 ** attempt) * 0.75
                    logger.warning(f"Network error ({type(exc).__name__}). Retrying in {backoff:.1f}s...")
                    await asyncio.sleep(backoff)
                else:
                    raise LLMOfflineError(f"Failed to connect to OmniRoute at {settings.OMNIROUTE_BASE_URL}: {type(exc).__name__}")

        raise last_error or LLMServiceError("Unknown failure executing LLM request.")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        fallback: Optional[str] = None,
        use_cache: bool = True,
        api_key: Optional[str] = None,
        timeout_seconds: Optional[float] = None
    ) -> str:
        """
        Executes a chat completion request with caching, exponential retries, and graceful fallback.
        Supports dedicated api_key override to isolate specific features (e.g. Chatbox).
        """
        selected_model = model or self.fast_model
        cache_key = self._generate_cache_key(selected_model, messages, temperature, schema_name=api_key or "")

        if use_cache:
            cached = self.get_from_cache(cache_key)
            if cached is not None:
                return str(cached)

        try:
            result = await self._call_api_with_retry(
                model=selected_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=api_key,
                timeout_override=timeout_seconds
            )
            if use_cache:
                self.set_cache(cache_key, result)
            return result
        except Exception as exc:
            logger.error(f"LLM chat error ({type(exc).__name__}): {exc}")
            if fallback is not None:
                return fallback
            raise exc

    async def chat_json(
        self,
        messages: List[Dict[str, str]],
        schema: Type[T],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        fallback: Optional[T] = None,
        max_repair_retries: int = 2,
        use_cache: bool = True
    ) -> T:
        """
        Executes structured JSON generation with Pydantic schema validation, repair retry, and graceful fallback.
        """
        selected_model = model or self.strong_model
        cache_key = self._generate_cache_key(selected_model, messages, temperature, schema.__name__)

        if use_cache:
            cached = self.get_from_cache(cache_key)
            if cached is not None:
                try:
                    return schema.model_validate(cached)
                except Exception:
                    pass

        # Prepare messages with JSON schema instructions
        schema_def = json.dumps(schema.model_json_schema(), indent=2)
        system_instruction = (
            f"You are a strict JSON generator. Your output must strictly adhere to the following JSON Schema:\n"
            f"{schema_def}\n"
            f"Respond ONLY with a valid raw JSON object. Do not include markdown code fences (like ```json), commentary, or explanations."
        )

        effective_messages = [{"role": "system", "content": system_instruction}] + messages

        for repair_attempt in range(max_repair_retries + 1):
            try:
                raw_response = await self._call_api_with_retry(
                    model=selected_model,
                    messages=effective_messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # Clean response (strip ```json fences if model outputs them)
                cleaned = raw_response.strip()
                if cleaned.startswith("```"):
                    lines = cleaned.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    cleaned = "\n".join(lines).strip()

                parsed_dict = json.loads(cleaned)
                validated_obj = schema.model_validate(parsed_dict)

                if use_cache:
                    self.set_cache(cache_key, validated_obj.model_dump())

                return validated_obj

            except (json.JSONDecodeError, ValidationError) as parse_exc:
                logger.warning(f"JSON validation attempt {repair_attempt + 1} failed: {parse_exc}")
                if repair_attempt < max_repair_retries:
                    # Append repair retry message
                    effective_messages.append({"role": "assistant", "content": raw_response})
                    effective_messages.append({
                        "role": "user",
                        "content": f"Your previous response caused validation error: {parse_exc}. Return ONLY corrected, valid JSON matching the schema."
                    })
                else:
                    if fallback is not None:
                        return fallback
                    raise LLMServiceError(f"Failed to produce valid JSON adhering to {schema.__name__}: {parse_exc}")
            except Exception as exc:
                logger.error(f"LLM chat_json error ({type(exc).__name__}): {exc}")
                if fallback is not None:
                    return fallback
                raise LLMOfflineError(f"AI service unavailable during chat_json: {exc}")

        if fallback is not None:
            return fallback
        raise LLMServiceError(f"Failed to generate valid {schema.__name__}")

llm_service = LLMService()
