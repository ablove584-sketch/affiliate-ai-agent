# AI Content Agent — GitHub Actions

وكيل محتوى آلي يعمل على GitHub Actions: يولّد منشورًا، يفحص التكرار على مستوى النص والفكرة والعنوان والكلمات المفتاحية، ثم ينشره إلى Telegram أو Webhook.

## المزايا
- تشغيل تلقائي كل 10 دقائق.
- توليد عبر أي API متوافق مع OpenAI Chat Completions.
- ذاكرة SQLite دائمة.
- منع تكرار النص والفكرة والزاوية.
- محاولات متعددة عند اكتشاف التكرار.
- Telegram Bot API وGeneric Webhook.
- DRY_RUN للاختبار.
- سجل للتشغيلات والأخطاء.
- GitHub Actions concurrency لمنع التشغيل المتوازي.
- Git commit تلقائي لقاعدة الذاكرة.

## الإعداد

1. ارفع الملفات إلى مستودع GitHub.
2. أضف Secrets:
   - `AI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `PUBLISH_WEBHOOK_URL` اختياري
   - `PUBLISH_WEBHOOK_SECRET` اختياري
3. أضف Variables عند الحاجة:
   - `AI_BASE_URL`
   - `AI_MODEL`
   - `CONTENT_TOPIC`
   - `CONTENT_STYLE`
   - `CONTENT_AUDIENCE`
   - `DUPLICATE_THRESHOLD`
   - `MAX_GENERATION_ATTEMPTS`
   - `PUBLISHERS`
4. شغّل Workflow يدويًا أول مرة باستخدام `dry_run=true`.
5. بعد التأكد، اجعل `DRY_RUN=false`.

## تشغيل محلي

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.agent --dry-run
```

## الاختبارات

```bash
python -m unittest discover -s tests -v
```

## منع التكرار

الوكيل يقارن المنشور المقترح مع الذاكرة السابقة باستخدام تشابه الكلمات، shingles، العنوان، الموضوع، الزاوية والكلمات المفتاحية. إذا تجاوزت النتيجة `DUPLICATE_THRESHOLD` يتم رفض المنشور وطلب فكرة أخرى من النموذج.

## ملاحظة مهمة عن كل 10 دقائق

GitHub Actions جدولة best-effort وليست مؤقتًا real-time. `*/10 * * * *` يجعل التشغيل مستحقًا كل 10 دقائق، لكن GitHub قد يؤخر التنفيذ عند الضغط. إذا كان المطلوب توقيتًا صارمًا جدًا، استخدم scheduler خارجيًا لاستدعاء Workflow.

## الأمان

لا تضع API keys داخل Git. استخدم GitHub Secrets، ويفضل جعل المستودع Private إذا كانت ذاكرة المحتوى مهمة.
