import os
import time
import io
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

OUTPUT_W, OUTPUT_H = 1280, 720

# 🔥 FIXED IMAGE (ALWAYS USE THIS)
FIXED_IMAGE_URL = "https://files.catbox.moe/4rk0j2.jpg"


async def get_thumb(videoid: str) -> str:
    # 🔥 UNIQUE FILE EVERY TIME (TELEGRAM CACHE FIX)
    cache_path = os.path.join(
        CACHE_DIR, f"{videoid}_{int(time.time())}.png"
    )

    img = None

    # ================= DOWNLOAD IMAGE =================
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(FIXED_IMAGE_URL) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    img = Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        img = None

    # ================= HARD FALLBACK (NO FILE, NO NET) =================
    if img is None:
        # solid dark background (never fails)
        img = Image.new("RGBA", (OUTPUT_W, OUTPUT_H), (30, 30, 30, 255))

    # ================= BUILD THUMB =================
    bg = ImageEnhance.Brightness(
        img.resize((OUTPUT_W, OUTPUT_H)).filter(ImageFilter.GaussianBlur(18))
    ).enhance(0.55)

    # center image
    center = img.resize((540, 270))
    mask = Image.new("L", center.size, 255)
    bg.paste(center, (370, 170), mask)

    bg.save(cache_path)
    return cache_path
