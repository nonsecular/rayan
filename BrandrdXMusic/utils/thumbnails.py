import os
import time
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

OUTPUT_W, OUTPUT_H = 1280, 720

# 🔥 FIXED IMAGE URL
FIXED_IMAGE_URL = "https://files.catbox.moe/4rk0j2.jpg"

# 🔥 LOCAL FALLBACK (MUST EXIST)
LOCAL_BG = "BrandrdXMusic/assets/thumb/bg.jpg"


async def get_thumb(videoid: str) -> str:
    # 🔥 UNIQUE FILE (TELEGRAM CACHE DEAD)
    cache_path = os.path.join(
        CACHE_DIR, f"{videoid}_{int(time.time())}.png"
    )

    img = None

    # ================= TRY ONLINE IMAGE =================
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FIXED_IMAGE_URL, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    img = Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        img = None

    # ================= FALLBACK (NO CRASH) =================
    if img is None:
        img = Image.open(LOCAL_BG).convert("RGBA")

    # ================= BUILD THUMB =================
    bg = ImageEnhance.Brightness(
        img.resize((OUTPUT_W, OUTPUT_H)).filter(ImageFilter.GaussianBlur(18))
    ).enhance(0.55)

    center = img.resize((540, 270))
    mask = Image.new("L", center.size, 255)
    bg.paste(center, (370, 170), mask)

    bg.save(cache_path)
    return cache_path
