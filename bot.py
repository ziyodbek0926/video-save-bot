import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
import asyncio
from config import TOKEN
from utils import download_instagram_content
from database import create_table, save_user
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

create_table()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom! Instagramdan rasm yoki video yuklab olish uchun Instagram postining URL manzilini yuboring.")

@dp.message_handler()
async def download_instagram_post(message: types.Message):
    post_url = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    logging.info(f"Foydalanuvchi {username} ({user_id}) quyidagi URL manzilni yubordi: {post_url}")

    save_user(user_id, username)

    # Instagramdan rasm yoki video URL'ni olish
    result = download_instagram_content(post_url)

    if result:
        if result.endswith('.mp4'):
            await message.answer_video(result)
        else:
            await message.answer_photo(result)
    else:
        await message.answer("Instagram postining URL manzili noto'g'ri yoki kontentni yuklab bo'lmadi. Iltimos, qayta urinib ko'ring.")

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
