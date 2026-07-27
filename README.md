# video-save-bot

YouTube, Instagram va Pinterest havolalaridan video va rasmlarni yuklab, to'g'ridan-to'g'ri Telegram orqali yetkazib beruvchi asinxron bot.

## Xususiyatlari

- **Uchta platforma** — YouTube (oddiy video va Shorts), Instagram (Reels, Post, TV), Pinterest (pin va `pin.it` qisqa havolalar).
- **Tezkor javob** — havola yuborilgach darhol "⏳ Yuklanmoqda..." xabari chiqadi, yuklash esa fonda, asinxron tarzda bajariladi.
- **Avtomatik tozalash** — fayl yuborilgach, serverdagi vaqtinchalik fayl va "Yuklanmoqda..." xabari o'zi o'chib ketadi.
- **50MB chegarasi** — Telegram bot API limitidan katta fayllar yuborilmaydi, o'rniga tushunarli xabar beriladi.
- **O'zbek tilidagi xatolik xabarlari** — yopiq profil, noto'g'ri havola yoki hajm chegarasi kabi holatlar aniq tushuntiriladi.
- **ffmpeg ixtiyoriy** — mavjud bo'lsa eng yuqori sifat (video+audio birlashtirilgan holda), bo'lmasa ham bot pastroqroq sifat bilan ishlayveradi.

## Texnologiyalar

| Texnologiya | Vazifasi |
|---|---|
| Python 3.11+ | Asosiy til |
| aiogram 3.x | Telegram bot freymvorki (asinxron) |
| yt-dlp | Media ma'lumotlarini olish va yuklash |
| pydantic-settings | `.env` orqali sozlamalarni boshqarish |
| ffmpeg *(ixtiyoriy)* | Video va audio oqimlarini birlashtirish |

## Loyiha tuzilishi

```
video-save-bot/
├── bot/
│   ├── main.py                 # Kirish nuqtasi — routerlarni ulaydi, pollingni boshlaydi
│   ├── core/
│   │   ├── config.py           # .env dan BOT_TOKEN, DOWNLOADS_DIR va h.k. ni o'qiydi
│   │   └── loader.py           # Bot va Dispatcher instansiyalari
│   ├── handlers/
│   │   └── media_handler.py    # /start va havola handlerlari
│   └── services/
│       └── downloader.py       # Platforma aniqlash + yt-dlp integratsiyasi
├── .env                         # Maxfiy sozlamalar (git'ga tushmaydi)
├── .env.example                 # Namuna sozlamalar fayli
├── requirements.txt
└── README.md
```

## O'rnatish

**1. Virtual muhit yarating va faollashtiring:**

```bash
python -m venv venv
source venv/Scripts/activate
```

**2. Kutubxonalarni o'rnating:**

```bash
pip install -r requirements.txt
```

**3. `.env` faylini yarating:**

```bash
cp .env.example .env
```

Fayl ichidagi `BOT_TOKEN` qiymatini [@BotFather](https://t.me/BotFather) dan olingan token bilan to'ldiring.

**4. *(Ixtiyoriy)* ffmpeg o'rnating** — pastdagi ["ffmpeg haqida"](#ffmpeg-haqida) bo'limiga qarang.

## Sozlamalar (`.env`)

| O'zgaruvchi | Majburiymi | Standart | Tavsif |
|---|---|---|---|
| `BOT_TOKEN` | Ha | — | [@BotFather](https://t.me/BotFather) dan olingan bot tokeni |
| `MAX_FILE_SIZE_MB` | Yo'q | `50` | Telegram bot API limiti — bundan katta fayllar yuborilmaydi |
| `DOWNLOADS_DIR` | Yo'q | `downloads` | Vaqtinchalik fayllar saqlanadigan papka |
| `FFMPEG_LOCATION` | Yo'q | — | ffmpeg PATH'da bo'lmasa, `ffmpeg.exe` turgan papkaning yo'li |

## Ishga tushirish

Har doim **loyiha ildizidan**, modul sifatida ishga tushiring (`bot/` papkasi ichidan emas):

```bash
python -m bot.main
```

## ffmpeg haqida

`yt-dlp` eng yuqori sifatli video uchun video va audio oqimlarini alohida yuklab, keyin ffmpeg orqali birlashtiradi. ffmpeg topilmasa ham bot ishlayveradi (tayyor, pastroqroq sifatli formatlar bilan) — lekin eng yaxshi natija uchun o'rnatish tavsiya etiladi.

- **PATH orqali o'rnatilgan bo'lsa**: terminalda `ffmpeg -version` ishlasa, qo'shimcha sozlash shart emas.
- **PATH'ga qo'shilmagan bo'lsa** (masalan, arxivni biror papkaga ochgan bo'lsangiz): `.env` fayliga qo'shing:

  ```
  FFMPEG_LOCATION=C:\Program Files\ffmpeg-master-latest-win64-gpl-shared\bin
  ```

## Qo'llab-quvvatlanadigan havolalar

| Platforma | Namuna havolalar |
|---|---|
| YouTube | `youtube.com/watch?v=...`, `youtube.com/shorts/...`, `youtu.be/...` |
| Instagram | `instagram.com/reel/...`, `instagram.com/reels/...`, `instagram.com/p/...`, `instagram.com/tv/...` |
| Pinterest | `pinterest.com/pin/...`, `pin.it/...` |

## Cheklovlar

- Fayl hajmi `MAX_FILE_SIZE_MB` dan katta bo'lsa, yuborilmaydi.
- Yopiq (private) profil yoki login talab qiladigan kontent yuklab bo'lmaydi.
- Bir nechta media (carousel post)larda hozircha faqat birinchi element yuklanadi.
- Har bir so'rov qayta yuklanadi — natijalar keshlanmaydi.

## Muammolarni bartaraf etish

**`ModuleNotFoundError: No module named 'bot'`**
`bot/` papkasi ichidan turib `python main.py` ishga tushirilganda shu xato chiqadi. Loyiha ildiziga qayting (`cd ..`) va `python -m bot.main` bilan ishga tushiring.

**`ffmpeg is not installed` xatosi**
ffmpeg o'rnatilmagan yoki PATH'da topilmayapti. Yuqoridagi ["ffmpeg haqida"](#ffmpeg-haqida) bo'limiga qarang.

**Instagram yoki Pinterest'dan yuklab bo'lmayapti**
Ko'pincha kontent yopiq profilga tegishli yoki login talab qiladi — bunday holatlarda bot mos xabar bilan javob beradi, bu kod xatosi emas.
