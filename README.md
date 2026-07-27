# video-save-bot

YouTube, Instagram va Pinterest havolalaridan video/rasm yuklab beruvchi Telegram bot.

## Talablar

- Python 3.11+
- [ffmpeg](https://ffmpeg.org/download.html) (video va audio oqimlarini birlashtirish uchun `yt-dlp`ga kerak) — PATH ga qo'shilgan bo'lishi kerak.

## O'rnatish

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`.env.example` faylidan nusxa oling va `BOT_TOKEN` qiymatini [@BotFather](https://t.me/BotFather) dan olingan token bilan to'ldiring:

```bash
copy .env.example .env
```

## Ishga tushirish

Loyiha ildizidan modul sifatida ishga tushiring:

```bash
python -m bot.main
```

## Tuzilma

```
bot/
├── core/
│   ├── config.py     # pydantic-settings orqali .env ni o'qiydi
│   └── loader.py     # Bot va Dispatcher instansiyalari
├── handlers/
│   └── media_handler.py  # /start va havola handlerlari
├── services/
│   └── downloader.py     # platforma aniqlash + yt-dlp integratsiyasi
└── main.py            # kirish nuqtasi (polling)
```

## Cheklovlar

- Fayl hajmi Telegram bot API limiti — 50MB (`.env` orqali `MAX_FILE_SIZE_MB` bilan sozlanadi) dan katta bo'lsa, yuborilmaydi.
- Yopiq (private) profil yoki login talab qiladigan kontent yuklab bo'lmaydi.
- Bir nechta media (carousel post)larda hozircha faqat birinchi element yuklanadi.
