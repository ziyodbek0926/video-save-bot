import logging
from aiogram import Bot, Dispatcher, types
import asyncio
from config import TOKEN
from utils import download_instagram_content
import os

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Start buyrug'i
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom! Instagramdan rasm yoki video yuklab olish uchun Instagram postining URL manzilini yuboring.")

# Instagram URL'larini qayta ishlash
@dp.message_handler()
async def download_instagram_post(message: types.Message):
    post_url = message.text
    logging.info(f"Foydalanuvchi {message.from_user.username} ({message.from_user.id}) quyidagi URL manzilni yubordi: {post_url}")

    # Instagramdan rasm yoki video URL'ni olish
    result = download_instagram_content(post_url)

    if result:
        # Fayl turi bo'yicha tekshirish va jo'natish
        if result.endswith('.mp4'):
            # Video bo'lsa, videoni yuborish
            await message.answer_video(types.InputFile(result))
        elif result.endswith('.jpg'):
            # Rasm bo'lsa, rasmni yuborish
            await message.answer_photo(types.InputFile(result))
        
        # Foydalanuvchiga fayl jo'natilgandan keyin faylni o'chirish
        os.remove(result)

        # O'chirilgandan keyin katalogni o'chirish
        try:
            os.rmdir(os.path.dirname(result))  # Katalog bo'sh bo'lsa, o'chirish
        except OSError:
            pass  # Agar katalogda boshqa fayllar bo'lsa, o'chirilmaydi

    else:
        await message.answer("Instagram postining URL manzili noto'g'ri yoki kontentni yuklab bo'lmadi. Iltimos, qayta urinib ko'ring.")

# Botni ishga tushirish
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
