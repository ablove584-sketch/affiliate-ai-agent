import os
import asyncio
import random
import requests
from telegram import Bot
from datetime import datetime

# المتغيرات من البيئة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# استخدام نموذج Qwen 2.5 (أحدث وأفضل)
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

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
    
    prompt = f"""أنت مساعد تسويقي محترف. اكتب إعلاناً جذاباً بالعربي عن: {product}

الشروط:
- استخدم 2-3 إيموجي
- اذكر ميزة واحدة رائعة
- اجعله 50-70 كلمة
- أضف في النهاية: 🛒 للرابط والتفاصيل: [اضغط هنا]

ابدأ الإعلان مباشرة."""

    try:
        output = query_huggingface(prompt)
        
        # استخراج النص
        if isinstance(output, list) and len(output) > 0:
            ad_text = output[0].get('generated_text', '')
        elif isinstance(output, dict):
            ad_text = output.get('generated_text', '')
        else:
            ad_text = str(output)
        
        # تنظيف النص
        ad_text = ad_text.strip()
        
        return ad_text if ad_text else "⚠️ لم يتم توليد الإعلان"
        
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
