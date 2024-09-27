import os
import requests
from bs4 import BeautifulSoup

# Instagram kontentini yuklab olish funktsiyasi
def download_instagram_content(post_url, save_folder="downloads"):
    response = requests.get(post_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Instagram sahifasida "og:image" yoki "og:video" URL'sini topish
        image_url = None
        video_url = None
        for tag in soup.find_all('meta'):
            if tag.get('property') == 'og:image':
                image_url = tag.get('content')
            elif tag.get('property') == 'og:video':
                video_url = tag.get('content')

        # Agar video bor bo'lsa, uni yuklash
        if video_url:
            return download_video(video_url, save_folder)
        
        # Agar faqat rasm bo'lsa, uni yuklash
        elif image_url:
            return download_image(image_url, save_folder)

    return None

def download_image(image_url, save_folder="downloads"):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Fayl nomini URL'dan olish
    file_name = image_url.split("/")[-1].split("?")[0]
    file_path = os.path.join(save_folder, file_name)

    # Rasmdan ma'lumotni olish va uni faylga yozish
    response = requests.get(image_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return file_path

def download_video(video_url, save_folder="downloads"):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Fayl nomini URL'dan olish
    file_name = video_url.split("/")[-1].split("?")[0]
    file_path = os.path.join(save_folder, file_name)

    # Videoni yuklab olish
    response = requests.get(video_url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    return file_path
