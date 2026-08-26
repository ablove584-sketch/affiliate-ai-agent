import os
import asyncio
import google.generativeai as genai
from telegram import Bot
from datetime import datetime

# الحصول على المتغيرات من البيئة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تهيئة الذكاء الاصطناعي (Gemini)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def generate_ad():
    """يطلب من الذكاء الاصطناعي كتابة إعلان لمنتج عشوائي"""
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
    
    import random
    product = random.choice(products)
    
    prompt = f"""
    أنت خبير تسويق بالعمولة. اكتب إعلاناً تسويقياً قصيراً ومثيراً (باللغة العربية) 
    عن: {product}
    
    التعليمات:
    - اجعل النص جذاباً ومشوقاً
    - استخدم 2-3 إيموجي مناسبة
    - اذكر ميزة أو ميزتين رائعتين للمنتج
    - اجعل الطول بين 50-100 كلمة
    - في النهاية أضف: \n\n🛒 للرابط والتفاصيل: [اضغط هنا]
    
    ابدأ الإعلان مباشرة بدون مقدمات.
    """
    
    response = model.generate_content(prompt)
    return response.text

async def send_to_telegram(message):
    """يرسل الإعلان إلى قناة تيليجرام"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message,
            parse_mode='Markdown'
        )
        print("✅ تم نشر الإعلان بنجاح على تيليجرام!")
        return True
    except Exception as e:
        print(f"❌ خطأ في النشر: {e}")
        return False

async def main():
    print("🤖 الوكيل يعمل الآن...")
    print(f"⏰ الوقت: {datetime.now()}")
    print("🧠 جاري توليد الإعلان...\n")
    
    ad_text = await generate_ad()
    print(f"📝 الإعلان المُولّد:\n{ad_text}\n")
    
    print(" جاري النشر على تيليجرام...")
    success = await send_to_telegram(ad_text)
    
    if success:
        print("\n🎉 المهمة اكتملت بنجاح!")
    else:
        print("\n️ حدث خطأ في النشر")

if __name__ == "__main__":
    asyncio.run(main())
