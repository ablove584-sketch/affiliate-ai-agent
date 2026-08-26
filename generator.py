import json
import requests
from .duplicate import fingerprint

SYSTEM = """أنت وكيل محتوى عربي محترف.
مهمتك إنتاج منشور واحد فقط.
يجب أن تكون الفكرة جديدة وليست إعادة صياغة لمحتوى سابق.
لا تكرر نفس المثال أو الزاوية أو البناء.
اكتب بالعربية الفصحى.
أعد JSON صالحًا فقط، بدون Markdown.
الحقول:
title, topic, angle, keywords, content, hashtags
keywords مصفوفة نصوص.
hashtags مصفوفة نصوص.
content منشور مكتمل وقابل للنشر.
"""

class AIGenerator:
    def __init__(self, settings):
        self.s = settings
        if not self.s.ai_api_key:
            raise RuntimeError("AI_API_KEY غير موجود")

    def generate(self, previous_posts, rejected_summaries=None):
        previous = []
        for p in previous_posts[:80]:
            previous.append({
                "title": p["title"],
                "topic": p["topic"],
                "angle": p["angle"],
                "keywords": p["keywords"],
            })

        user = {
            "language": self.s.content_language,
            "main_topic": self.s.content_topic,
            "style": self.s.content_style,
            "audience": self.s.content_audience,
            "max_hashtags": self.s.hashtags_max,
            "previous_content_to_avoid": previous,
            "recent_rejections": rejected_summaries or [],
            "rules": [
                "لا تعيد نفس الفكرة حتى لو تغيرت الكلمات.",
                "اختر زاوية مختلفة جذريًا عن آخر المنشورات.",
                "لا تستخدم عنوانًا قريبًا من العناوين السابقة.",
                "اجعل المنشور مفيدًا وليس مجرد حشو.",
                "لا تخترع أرقامًا أو حقائق دقيقة غير مؤكدة.",
                "الهاشتاجات بحد أقصى العدد المحدد."
            ]
        }

        r = requests.post(
            f"{self.s.ai_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.s.ai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.s.ai_model,
                "temperature": 0.95,
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": json.dumps(user, ensure_ascii=False)}
                ],
            },
            timeout=90,
        )
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()
        post = json.loads(content)

        required = ["title", "topic", "angle", "keywords", "content", "hashtags"]
        missing = [x for x in required if x not in post]
        if missing:
            raise ValueError(f"حقول ناقصة: {missing}")

        post["keywords"] = list(dict.fromkeys(map(str, post["keywords"])))
        post["hashtags"] = list(dict.fromkeys(map(str, post["hashtags"])))[:self.s.hashtags_max]
        post["fingerprint"] = fingerprint(post)
        return post
