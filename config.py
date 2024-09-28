from dotenv import load_dotenv
import os

# .env faylini yuklash
load_dotenv()

# Tokenni olish
TOKEN = os.getenv('TOKEN')

# Token noto'g'ri bo'lmasligini tekshirish
if not TOKEN:
    raise ValueError("Bot tokeni .env faylidan yuklanmadi.")
