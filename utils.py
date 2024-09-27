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

        # Agar post video bo'lsa, videoni yuklab olish
        if post.is_video:
            video_file = loader.download_post(post, target=target_dir)
            for file in os.listdir(target_dir):
                if file.endswith(".mp4"):
                    return os.path.join(target_dir, file)

        # Agar post rasm bo'lsa, rasmni yuklab olish
        elif post.is_downloadable:
            for file in os.listdir(target_dir):
                if file.endswith(".jpg"):
                    return os.path.join(target_dir, file)
    
    except Exception as e:
        print(f"Instagram kontentini yuklab olishda xato: {e}")
        return None
