import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
import asyncio
from config import TOKEN
from utils import download_instagram_content
from database import create_table, save_user

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Jadval yaratish
create_table()

# Start buyrug'i
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom! Instagramdan rasm yoki video yuklab olish uchun Instagram postining URL manzilini yuboring.")

# Instagram URL'larini qayta ishlash
@dp.message_handler()
async def download_instagram_post(message: types.Message):
    post_url = message.text
    logging.info(f"Foydalanuvchi {message.from_user.username} ({message.from_user.id}) quyidagi URL manzilni yubordi: {post_url}")

    # Foydalanuvchini bazaga qo'shish
    save_user(message.from_user.id, message.from_user.username)

    # Instagramdan rasm yoki video yuklab olish
    result = download_instagram_content(post_url)

    # Agar yuklab olish muvaffaqiyatli bo'lsa
    if result:
        # Yuklangan faylni jo'natish
        with open(result, 'rb') as file:
            if result.endswith(('.mp4', '.avi', '.mov')):
                await message.answer_video(file)
            else:
                await message.answer_photo(file)
    else:
        await message.answer("Instagram postining URL manzili noto'g'ri yoki kontentni yuklab bo'lmadi. Iltimos, qayta urinib ko'ring.")

# Botni ishga tushirish
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
