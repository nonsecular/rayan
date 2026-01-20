import os
import re
import time
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

# ===================== CONSTANTS =====================

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

OUTPUT_W, OUTPUT_H = 1280, 720

# 🔥 BACKGROUND IMAGE (PUT YOUR IMAGE HERE)
BG_IMAGE = "BrandrdXMusic/assets/thumb/bg.jpg"

PANEL_W, PANEL_H = 763, 545
PANEL_X = (OUTPUT_W - PANEL_W) // 2
PANEL_Y = 88

TRANSPARENCY = 170
INNER_OFFSET = 36

THUMB_W, THUMB_H = 542, 273
THUMB_X = PANEL_X + (PANEL_W - THUMB_W) // 2
THUMB_Y = PANEL_Y + INNER_OFFSET

TITLE_X = 377
META_X = 377
TITLE_Y = THUMB_Y + THUMB_H + 10
META_Y = TITLE_Y + 45

BAR_X, BAR_Y = 388, META_Y + 45
BAR_RED_LEN = 280
BAR_TOTAL_LEN = 480

ICONS_W, ICONS_H = 415, 45
ICONS_X = PANEL_X + (PANEL_W - ICONS_W) // 2
ICONS_Y = BAR_Y + 48

MAX_TITLE_WIDTH = 580

FONT_TITLE_PATH = "BrandrdXMusic/assets/thumb/font2.ttf"
FONT_REGULAR_PATH = "BrandrdXMusic/assets/thumb/font.ttf"
ICONS_PATH = "BrandrdXMusic/assets/thumb/play_icons.png"

# ===================== HELPERS =====================

def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    if font.getlength(text) <= max_w:
        return text
    for i in range(len(text), 0, -1):
        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis
    return ellipsis


def load_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# ===================== MAIN =====================

async def get_thumb(videoid: str) -> str:

    cache_path = os.path.join(CACHE_DIR, f"{videoid}_bg.png")
    if os.path.exists(cache_path):
        return cache_path

    # ===================== YOUTUBE DATA (ONLY TEXT) =====================

    try:
        search = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await search.next())["result"][0]
        title = re.sub(r"\s+", " ", data.get("title", "Unknown Title")).strip()
        duration = data.get("duration")
        views = data.get("viewCount", {}).get("short", "Unknown Views")
    except Exception:
        title = "Unsupported Title"
        duration = None
        views = "Unknown Views"

    is_live = not duration or str(duration).lower() in ("", "live", "live now")
    duration_text = "Live" if is_live else duration

    # ===================== IMAGE PROCESS =====================

    # 🔥 BACKGROUND (BLUR + DARK)
    base_bg = Image.open(BG_IMAGE).resize((OUTPUT_W, OUTPUT_H)).convert("RGBA")
    bg = ImageEnhance.Brightness(
        base_bg.filter(ImageFilter.GaussianBlur(16))
    ).enhance(0.55)

    # 🔥 FROSTED GLASS PANEL
    panel_crop = bg.crop((PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H))
    overlay = Image.new("RGBA", (PANEL_W, PANEL_H), (255, 255, 255, TRANSPARENCY))
    frosted = Image.alpha_composite(panel_crop, overlay)

    mask = Image.new("L", (PANEL_W, PANEL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W, PANEL_H), 50, fill=255)
    bg.paste(frosted, (PANEL_X, PANEL_Y), mask)

    draw = ImageDraw.Draw(bg)

    title_font = load_font(FONT_TITLE_PATH, 32)
    regular_font = load_font(FONT_REGULAR_PATH, 18)

    # 🔥 CENTER IMAGE (SHARP – SAME BG IMAGE)
    inner = Image.open(BG_IMAGE).resize((THUMB_W, THUMB_H)).convert("RGBA")
    tmask = Image.new("L", (THUMB_W, THUMB_H), 0)
    ImageDraw.Draw(tmask).rounded_rectangle((0, 0, THUMB_W, THUMB_H), 20, fill=255)
    bg.paste(inner, (THUMB_X, THUMB_Y), tmask)

    # ===================== TEXT =====================

    draw.text(
        (TITLE_X, TITLE_Y),
        trim_to_width(title, title_font, MAX_TITLE_WIDTH),
        fill="black",
        font=title_font,
    )

    draw.text(
        (META_X, META_Y),
        f"YouTube • {views}",
        fill="black",
        font=regular_font,
    )

    # ===================== PROGRESS BAR =====================

    draw.line([(BAR_X, BAR_Y), (BAR_X + BAR_RED_LEN, BAR_Y)], fill="red", width=6)
    draw.line(
        [(BAR_X + BAR_RED_LEN, BAR_Y), (BAR_X + BAR_TOTAL_LEN, BAR_Y)],
        fill="gray",
        width=5,
    )
    draw.ellipse(
        [
            (BAR_X + BAR_RED_LEN - 7, BAR_Y - 7),
            (BAR_X + BAR_RED_LEN + 7, BAR_Y + 7),
        ],
        fill="red",
    )

    draw.text((BAR_X, BAR_Y + 15), "00:00", fill="black", font=regular_font)
    draw.text(
        (BAR_X + BAR_TOTAL_LEN - 70, BAR_Y + 15),
        duration_text,
        fill="red" if is_live else "black",
        font=regular_font,
    )

    # ===================== ICONS =====================

    if os.path.isfile(ICONS_PATH):
        icons = Image.open(ICONS_PATH).resize((ICONS_W, ICONS_H)).convert("RGBA")
        bg.paste(icons, (ICONS_X, ICONS_Y), icons)

    # ===================== SAVE =====================

    bg.save(cache_path)
    return cache_path
