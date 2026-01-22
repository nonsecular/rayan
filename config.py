import re
import os
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ================= BASIC ================= #

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_DB_URI = getenv("MONGO_DB_URI")
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME")
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 999999))

#LOGGER_ID = int(getenv("LOGGER_ID", "-1003530337097"))
LOGGER_ID = -1002276415311
OWNER_ID = int(getenv("OWNER_ID", 0))

LOG = int(getenv("LOG", 1))

# ================= HEROKU ================= #

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ================= API ================= #

API_URL = getenv("API_URL", "https://api.thequickearn.xyz")
VIDEO_API_URL = getenv("VIDEO_API_URL", "https://api.video.thequickearn.xyz")
API_KEY = getenv("API_KEY", "30DxNexGenBotsfcfad8")

# ================= GIT ================= #

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/nonsecular/rayan",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN")

# ================= SUPPORT ================= #

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/HMMMLLLLL")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/iscamz")

# ================= ASSISTANT ================= #

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_GCAST = getenv("AUTO_GCAST")
AUTO_GCAST_MSG = getenv("AUTO_GCAST_MSG", "")

ASSISTANT_USERNAME = "UnknownAura"        # WITHOUT @
ASSISTANT_NAME = "Unknown Aura"


# ================= SPOTIFY ================= #

SPOTIFY_CLIENT_ID = getenv(
    "SPOTIFY_CLIENT_ID",
    "bcfe26b0ebc3428882a0b5fb3e872473"
)
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET",
    "907c6a054c214005aeae1fd752273cc4"
)

# ================= LIMITS ================= #

SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", 999))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 999))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", 999))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", 999999))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

# ================= STRING SESSIONS ================= #

STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ================= GLOBAL STATES ================= #

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ================= START MEDIA ================= #

START_IMG_URL = getenv(
    "START_IMG_URL",
    "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
)

START_VID_URL = getenv(
    "START_VID_URL",
    "https://files.catbox.moe/m8wvfi.mp4"
)

# ================= STICKERS ================= #

STICKERS = [
    "CAACAgQAAyEFAASQEqrdAAIJs2jnyuMgspsf42Mcbh_5BzL_6gNLAAI3DgAC1nJYUMpU4o2QJkYtHgQ",
    "CAACAgUAAyEFAASQEqrdAAIJr2jnyeFTLUZlJzl1XKVQBSKOPQe6AAKECwACNcE4V12oPuGMNguiHgQ",
    "CAACAgQAAyEFAASQEqrdAAIJrGjnybC2lswXSzPELCuuut8t9SaFAAKiDgACYl1ZUEhWrJQdUTQ-HgQ",
]

AYU = [
    "CAACAgUAAyEFAASwkF6wAAIzz2jnx8vHV0DDuGuentmq00DMS59RAALGCAAC0v05V82aflzlC23sHgQ",
    "CAACAgUAAxkBAAIlv2jnx6f3e7RYjpCC72eI4hGPicHwAAKKCgACa18xV4AnhAOM68fJHgQ"
]

# ================= OTHER IMAGES ================= #

PING_IMG_URL = getenv(
    "PING_IMG_URL",
    "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
)

PLAYLIST_IMG_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
STATS_IMG_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
