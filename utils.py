import instaloader

def download_instagram_content(post_url):
    loader = instaloader.Instaloader()
    
    # Instagram postining shortcode'ini URL'dan ajratib olish
    try:
        shortcode = post_url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Video yoki rasmni yuklash
        if post.is_video:
            video_url = post.video_url
            return video_url
        else:
            image_url = post.url
            return image_url

    except Exception as e:
        print(f"Xato yuz berdi: {e}")
        return None
