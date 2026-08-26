import os
import asyncio
import json
import random
from datetime import datetime
from telegram import Bot
import google.generativeai as genai

# ============ الإعدادات ============
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HISTORY_FILE = "post_history.json"

# تهيئة Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# ============ أنواع المحتوى ============
CONTENT_TYPES = [
    {
        "name": "نصيحة",
        "prompt": "اكتب نصيحة عملية ومفيدة في مجال {field} باللغة العربية. اجعلها قصيرة (30-50 كلمة)، واضحة، ومباشرة. استخدم إيموجي واحد مناسب في البداية."
    },
    {
        "name": "حقيقة",
        "prompt": "شارك حقيقة مدهشة وغير معروفة عن {field} باللغة العربية. اجعلها قصيرة (30-50 كلمة) ومثيرة للاهتمام. استخدم إيموجي واحد في البداية."
    },
    {
        "name": "اقتباس",
        "prompt": "اكتب اقتباساً ملهماً وقصيراً عن {field} باللغة العربية (20-40 كلمة). أضف في النهاية اسم قائله أو 'مجهول'. استخدم إيموجي واحد."
    },
    {
        "name": "لغز",
        "prompt": "اكتب لغزاً ذكياً وممتعاً عن {field} باللغة العربية. اطرح اللغز ثم اكتب الإجابة في سطر جديد بعد كلمة 'الإجابة:'. اجعله قصيراً (40-60 كلمة)."
    },
    {
        "name": "معلومة",
        "prompt": "شارك معلومة علمية أو تقنية مفيدة عن {field} باللغة العربية. اجعلها دقيقة وقصيرة (40-60 كلمة). استخدم إيموجي واحد."
    },
    {
        "name": "تحفيز",
        "prompt": "اكتب رسالة تحفيزية قصيرة وقوية عن {field} باللغة العربية (30-50 كلمة). اجعلها ملهمة ومفعمة بالطاقة. استخدم إيموجي واحد."
    },
    {
        "name": "سؤال",
        "prompt": "اطرح سؤالاً تفكيرياً مثيراً للاهتمام عن {field} باللغة العربية (20-40 كلمة). اجعل القارئ يفكر بعمق. أضف في النهاية: 'شاركنا رأيك في التعليقات! 💬'"
    }
]

# ============ المجالات ============
FIELDS = [
    "التكنولوجيا والذكاء الاصطناعي",
    "التطوير الذاتي والنجاح",
    "الصحة واللياقة البدنية",
    "التسويق والأعمال",
    "البرمجة والتقنية",
    "القراءة والتعلم",
    "الإبداع والابتكار",
    "العلاقات الاجتماعية",
    "إدارة الوقت والإنتاجية",
    "الريادة وريادة الأعمال"
]

# ============ إدارة التاريخ ============
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"posts": [], "last_type": None, "last_field": None}

def save_history(history):
    # الاحتفاظ بآخر 100 منشور فقط
    history["posts"] = history["posts"][-100:]
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_unique_content(history):
    """اختيار نوع ومجال مختلفين عن آخر منشور"""
    # اختيار نوع مختلف
    available_types = [t for t in CONTENT_TYPES if t["name"] != history.get("last_type")]
    content_type = random.choice(available_types)
    
    # اختيار مجال مختلف
    available_fields = [f for f in FIELDS if f != history.get("last_field")]
    field = random.choice(available_fields)
    
    return content_type, field

# ============ توليد المحتوى ============
async def generate_content():
    history = load_history()
    content_type, field = get_unique_content(history)
    
    prompt = content_type["prompt"].format(field=field)
    prompt += "\n\nمهم: لا تكرر محتوى سابقاً. كن إبداعياً ومبتكراً."
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # تحديث التاريخ
        history["posts"].append({
            "type": content_type["name"],
            "field": field,
            "text": text,
            "time": datetime.now().isoformat()
        })
        history["last_type"] = content_type["name"]
        history["last_field"] = field
        save_history(history)
        
        # إضافة توقيع النوع
        footer = f"\n\n━━━━━━━━━━━━\n📌 {content_type['name']} | {field}"
        return text + footer
        
    except Exception as e:
        return f"❌ خطأ في توليد المحتوى: {str(e)}"

# ============ النشر على تيليجرام ============
async def send_to_telegram(message):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message,
            parse_mode='Markdown'
        )
        print("✅ تم النشر بنجاح!")
        return True
    except Exception as e:
        print(f"❌ خطأ في النشر: {e}")
        return False

# ============ التشغيل الرئيسي ============
async def main():
    print("🤖 وكيل المحتوى يعمل...")
    print(f"⏰ {datetime.now()}")
    print("🧠 جاري توليد محتوى جديد...\n")
    
    content = await generate_content()
    print(f"📝 المحتوى:\n{content}\n")
    
    print(" جاري النشر على تيليجرام...")
    await send_to_telegram(content)
    
    print("\n🎉 اكتملت المهمة!")

if __name__ == "__main__":
    asyncio.run(main())
