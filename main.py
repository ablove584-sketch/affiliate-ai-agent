import os
import asyncio
import requests
from telegram import Bot
from datetime import datetime
from huggingface_hub import InferenceClient

# الحصول على المتغيرات من البيئة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# التحقق من وجود المفتاح
if not HUGGINGFACE_TOKEN:
    raise ValueError(" HUGGINGFACE_TOKEN غير موجود في GitHub Secrets!")

# تهيئة العميل مع المفتاح
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HUGGINGFACE_TOKEN
)

async def generate_ad():
    """يطلب من الذكاء الاصطناعي كتابة إعلان"""
    products = [
        "سماعة بلوتوث لاسلكية",
        "شاحن لاسلكي سريع",
        "كاميرا مراقبة ذكية",
        "مصباح LED ذكي",
        "أداة مطبخ متعددة الاستخدامات",
        "منظم كابلات ذكي",
        "مقياس حرارة ذكي للمطبخ"
    ]
    
    import random
    product = random.choice(products)
    
    prompt = f"""[INST] اكتب إعلان تسويقي جذاب ومختصر بالعربي عن: {product}
- استخدم 2-3 إيموجي
- اذكر ميزة واحدة رائعة
- اجعله 50-70 كلمة
- أضف في النهاية: 🛒 للرابط والتفاصيل: [اضغط هنا]
[/INST]"""

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=200,
            temperature=0.7
        )
        return response
    except Exception as e:
        return f"❌ خطأ في توليد الإعلان: {e}"

async def send_to_telegram(message):
    """يرسل الإعلان إلى قناة تيليجرام"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message
        )
        print("✅ تم نشر الإعلان بنجاح على تيليجرام!")
        return True
    except Exception as e:
        print(f"❌ خطأ في النشر: {e}")
        return False

async def main():
    print(" الوكيل يعمل الآن...")
    print(f"⏰ الوقت: {datetime.now()}")
    print("🧠 جاري توليد الإعلان...\n")
    
    ad_text = await generate_ad()
    print(f"📝 الإعلان المُولّد:\n{ad_text}\n")
    
    print("📤 جاري النشر على تيليجرام...")
    success = await send_to_telegram(ad_text)
    
    if success:
        print("\n🎉 المهمة اكتملت بنجاح!")
    else:
        print("\n⚠️ حدث خطأ في النشر")

if __name__ == "__main__":
    asyncio.run(main())
