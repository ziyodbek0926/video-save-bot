import instaloader
import os

def download_instagram_content(post_url):
    try:
        loader = instaloader.Instaloader()

        # Post shortcode ni olish
        shortcode = post_url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Fayllarni saqlash uchun katalog yaratish
        target_dir = f"{post.owner_username}__{shortcode}"
        os.makedirs(target_dir, exist_ok=True)

        # Fayl ro'yxatini tayyorlash
        downloaded_files = {'images': [], 'videos': []}  # Rasm va video uchun ro'yxat

        # Yuklab olish
        loader.download_post(post, target=target_dir)

        # Yuklangan fayllarni tekshirish
        for file in os.listdir(target_dir):
            if file.endswith(".mp4"):
                downloaded_files['videos'].append(os.path.join(target_dir, file))
            elif file.endswith(".jpg"):
                downloaded_files['images'].append(os.path.join(target_dir, file))

        return downloaded_files  # Yuklangan fayllar ro'yxatini qaytarish

    except Exception as e:
        print(f"Instagram kontentini yuklab olishda xato: {e}")
        return None
