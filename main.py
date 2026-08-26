import os
import asyncio
import requests
from telegram import Bot
from huggingface_hub import InferenceClient

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

client = InferenceClient(token=HUGGINGFACE_TOKEN)

async def generate_ad():
    products = ["سماعة بلوتوث", "شاحن لاسلكي", "كاميرا ذكية"]
    import random
    product = random.choice(products)
    
    prompt = f"اكتب إعلان تسويقي جذاب بالعربي عن: {product} - استخدم ايموجي - أضف 🛒 للرابط في النهاية"
    
    response = client.text_generation(
        prompt,
        model="mistralai/Mistral-7B-Instruct-v0.3",
        max_new_tokens=150
    )
    return response

async def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
    print("✅ تم النشر!")

async def main():
    print("🤖 الوكيل يعمل...")
    ad = await generate_ad()
    print(ad)
    await send_to_telegram(ad)

if __name__ == "__main__":
    asyncio.run(main())
