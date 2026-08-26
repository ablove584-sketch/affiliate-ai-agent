import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def as_bool(value, default=False):
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}

@dataclass(frozen=True)
class Settings:
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_base_url: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    ai_model: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    content_language: str = os.getenv("CONTENT_LANGUAGE", "ar")
    content_topic: str = os.getenv("CONTENT_TOPIC", "العلوم والتقنية وتطوير الذات")
    content_style: str = os.getenv("CONTENT_STYLE", "احترافي، واضح، مفيد، غير مكرر")
    content_audience: str = os.getenv("CONTENT_AUDIENCE", "الجمهور العربي العام")
    hashtags_max: int = int(os.getenv("CONTENT_HASHTAGS_MAX", "5"))
    duplicate_threshold: float = float(os.getenv("DUPLICATE_THRESHOLD", "0.78"))
    max_generation_attempts: int = int(os.getenv("MAX_GENERATION_ATTEMPTS", "6"))
    memory_lookback: int = int(os.getenv("MEMORY_LOOKBACK", "1000"))
    publishers: tuple = tuple(x.strip() for x in os.getenv("PUBLISHERS", "telegram").split(",") if x.strip())
    dry_run: bool = as_bool(os.getenv("DRY_RUN"), False)
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    publish_webhook_url: str = os.getenv("PUBLISH_WEBHOOK_URL", "")
    publish_webhook_secret: str = os.getenv("PUBLISH_WEBHOOK_SECRET", "")
