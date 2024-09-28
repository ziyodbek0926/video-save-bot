import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import Throttled
from config import TOKEN
from utils import download_instagram_content
from database import save_user, remove_user_data

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# Bot va dispatcher yaratish
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Cheklov parametrlari (soniyalar)
RATE_LIMIT = 15  # Foydalanuvchining 15 soniyada 2 ta URL yuborishi mumkin
user_timestamps = {}  # Foydalanuvchilar vaqtini kuzatish uchun

# /start buyrug'iga javob
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom! Instagram post manzilini yuboring, biz rasm yoki videoni yuklab beramiz.")

# Cheklovga tushganda foydalanuvchiga xabar berish
@dp.throttled(rate=RATE_LIMIT, key="instagram_post")
async def rate_limit_handler(message: types.Message, throttled: Throttled):
    time_left = int(throttled.rate - throttled.delta)  # Qancha vaqt qoldi
    await message.answer(f"Juda ko'p so'rov yubordingiz. Iltimos {time_left} soniya kuting.")

# Instagram URL manzilini qabul qilish va uni yuklab berish
@dp.message_handler()
async def download_instagram_post(message: types.Message):
    user_id = message.from_user.id  # Foydalanuvchi ID si
    username = message.from_user.username  # Foydalanuvchi nomi
    post_url = message.text  # Foydalanuvchi yuborgan URL

    logging.info(f"Foydalanuvchi {username} ({user_id}) URL manzilini yubordi: {post_url}")

    # Cheklov: foydalanuvchi oxirgi marta so'rov yuborgan vaqti
    if user_id in user_timestamps:
        time_since_last = asyncio.get_event_loop().time() - user_timestamps[user_id]
        if time_since_last < RATE_LIMIT:
            time_left = int(RATE_LIMIT - time_since_last)
            await message.answer(f"Iltimos {time_left} soniya kuting va keyinroq yana so'rov yuboring.")
            return

    # Foydalanuvchi vaqtini yangilash
    user_timestamps[user_id] = asyncio.get_event_loop().time()

    # Foydalanuvchi ma'lumotlarini bazaga saqlash
    save_user(user_id, username)

    # Instagramdan kontent yuklab olish
    try:
        content_dict = download_instagram_content(post_url)  # Kontent yuklash funksiyasi

        if content_dict:
            # Rasm va videolarni jo'natish
            for video in content_dict.get('videos', []):
                with open(video, 'rb') as vid_file:
                    await message.answer_video(vid_file)
                await asyncio.sleep(1)  # Har bir fayl jo'natilgandan keyin biroz kutish

            for image in content_dict.get('images', []):
                with open(image, 'rb') as img_file:
                    await message.answer_photo(img_file)
                await asyncio.sleep(1)  # Har bir fayl jo'natilgandan keyin biroz kutish

        else:
            await message.answer("Kontentni olishda xatolik yuz berdi. URL manzilini tekshiring.")

    except Exception as e:
        logging.error(f"Instagram kontentini yuklashda xato: {e}")
        await message.answer("Instagram kontentini yuklashda xatolik yuz berdi.")

    # Foydalanuvchi ma'lumotlarini fayl jo'natilgandan keyin o'chirish
    remove_user_data(user_id)

# Botni ishga tushirish
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())

