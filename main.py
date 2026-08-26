import os
import asyncio
import random
from telegram import Bot
from datetime import datetime
import google.generativeai as genai

# المتغيرات من البيئة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تهيئة Gemini
genai.configure(api_key=GEMINI_API_KEY)

# استخدام النموذج الصحيح
model = genai.GenerativeModel('gemini-2.0-flash')

async def generate_ad():
    products = [
        "سماعة بلوتوث لاسلكية",
        "شاحن لاسلكي سريع",
        "كاميرا مراقبة ذكية",
        "مصباح LED ذكي",
        "أداة مطبخ متعددة الاستخدامات",
        "منظم كابلات ذكي",
        "مقياس حرارة ذكي للمطبخ",
        "فرشاة تنظيف كهربائية"
    ]
    
    product = random.choice(products)
    
    prompt = f"""اكتب إعلان تسويقي جذاب ومختصر بالعربي عن: {product}

الشروط:
- استخدم 2-3 إيموجي
- اذكر ميزة واحدة رائعة
- اجعله 50-70 كلمة
- أضف في النهاية: 🛒 للرابط والتفاصيل: [اضغط هنا]

ابدأ الإعلان مباشرة."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

async def send_to_telegram(message):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message
        )
        print("✅ تم النشر بنجاح!")
        return True
    except Exception as e:
        print(f" خطأ في النشر: {e}")
        return False

async def main():
    print(" الوكيل يعمل...")
    print(f" {datetime.now()}")
    
    ad = await generate_ad()
    print(f"\n الإعلان:\n{ad}\n")
    
    await send_to_telegram(ad)

if __name__ == "__main__":
    asyncio.run(main())
