import hashlib
import hmac
import json
import requests

class TelegramPublisher:
    name = "telegram"

    def __init__(self, settings):
        self.s = settings

    def publish(self, post):
        if not self.s.telegram_bot_token or not self.s.telegram_chat_id:
            raise RuntimeError("Telegram credentials غير مكتملة")
        text = f'*{post["title"]}*\n\n{post["content"]}\n\n{" ".join(post["hashtags"])}'
        r = requests.post(
            f"https://api.telegram.org/bot{self.s.telegram_bot_token}/sendMessage",
            json={
                "chat_id": self.s.telegram_chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False,
            },
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

class WebhookPublisher:
    name = "webhook"

    def __init__(self, settings):
        self.s = settings

    def publish(self, post):
        if not self.s.publish_webhook_url:
            raise RuntimeError("PUBLISH_WEBHOOK_URL غير موجود")
        body = {
            "title": post["title"],
            "topic": post["topic"],
            "angle": post["angle"],
            "content": post["content"],
            "hashtags": post["hashtags"],
        }
        headers = {"Content-Type": "application/json"}
        if self.s.publish_webhook_secret:
            raw = json.dumps(body, ensure_ascii=False, sort_keys=True).encode()
            signature = hmac.new(
                self.s.publish_webhook_secret.encode(), raw, hashlib.sha256
            ).hexdigest()
            headers["X-Content-Agent-Signature"] = signature
        r = requests.post(
            self.s.publish_webhook_url, json=body, headers=headers, timeout=30
        )
        r.raise_for_status()
        return r.json() if "application/json" in r.headers.get("content-type", "") else {"status": r.status_code}

def build_publishers(settings):
    mapping = {"telegram": TelegramPublisher, "webhook": WebhookPublisher}
    result = []
    for name in settings.publishers:
        cls = mapping.get(name)
        if not cls:
            raise ValueError(f"Publisher غير معروف: {name}")
        result.append(cls(settings))
    if not result:
        raise RuntimeError("لم يتم اختيار أي Publisher")
    return result
