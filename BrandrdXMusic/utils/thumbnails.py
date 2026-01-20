import os
import time
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

OUTPUT_W, OUTPUT_H = 1280, 720
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# 🔥 FIXED IMAGE (ALWAYS THIS)
FIXED_IMAGE_URL = "https://files.catbox.moe/4rk0j2.jpg"

async def get_thumb(videoid: str) -> str:
    # 🔥 UNIQUE FILE EVERY TIME (NO TELEGRAM CACHE)
    cache_path = os.path.join(
        CACHE_DIR, f"{videoid}_{int(time.time())}.png"
    )

    # 🔥 DOWNLOAD FIXED IMAGE
    resp = requests.get(FIXED_IMAGE_URL, timeout=10)
    img = Image.open(BytesIO(resp.content)).convert("RGBA")

    # BACKGROUND
    bg = ImageEnhance.Brightness(
        img.resize((OUTPUT_W, OUTPUT_H)).filter(ImageFilter.GaussianBlur(18))
    ).enhance(0.55)

    # CENTER IMAGE
    center = img.resize((540, 270))
    mask = Image.new("L", center.size, 255)
    bg.paste(center, (370, 170), mask)

    bg.save(cache_path)
    return cache_path
