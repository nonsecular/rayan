import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BrandrdXMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.utils import seconds_to_min, time_to_seconds
from BrandrdXMusic.utils.channelplay import get_channeplayCB
from BrandrdXMusic.utils.decorators.language import languageCB
from BrandrdXMusic.utils.decorators.play import PlayWrapper
from BrandrdXMusic.utils.formatters import formats
from BrandrdXMusic.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from BrandrdXMusic.utils.logger import play_logs
from BrandrdXMusic.utils.stream.stream import stream
from BrandrdXMusic.utils.thumbnails import get_thumb   # 🔥 FIX
from config import BANNED_USERS, lyrical, AYU


@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
        ]
    )
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    mystic = await message.reply_sticker(
        _["play_2"].format(channel) if channel else random.choice(AYU)
    )

    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # ================= TELEGRAM MEDIA =================

    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )

    # ---------------- TELEGRAM AUDIO ----------------
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(_["play_5"])
        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
            )

        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            details = {
                "title": await Telegram.get_filename(audio_telegram, audio=True),
                "link": await Telegram.get_link(message),
                "path": file_path,
                "dur": await Telegram.get_duration(audio_telegram, file_path),
            }
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                streamtype="telegram",
                forceplay=fplay,
            )
            return await mystic.delete()

    # ---------------- TELEGRAM VIDEO ----------------
    if video_telegram:
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])

        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            details = {
                "title": await Telegram.get_filename(video_telegram),
                "link": await Telegram.get_link(message),
                "path": file_path,
                "dur": await Telegram.get_duration(video_telegram, file_path),
            }
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=True,
                streamtype="telegram",
                forceplay=fplay,
            )
            return await mystic.delete()

    # ================= URL / SEARCH =================

    if url:
        if await YouTube.exists(url):
            if "playlist" in url:
                details = await YouTube.playlist(
                    url, config.PLAYLIST_FETCH_LIMIT, user_id
                )
                plist_type = "yt"
                plist_id = url.split("=")[-1]
                img = config.PLAYLIST_IMG_URL
                cap = _["play_9"]
            else:
                details, track_id = await YouTube.track(url)
                img = await get_thumb(track_id)   # 🔥 FIX
                cap = _["play_10"].format(
                    details["title"],
                    details["duration_min"],
                )
                streamtype = "youtube"

        elif await Spotify.valid(url):
            details, track_id = await Spotify.track(url)
            img = await get_thumb(track_id)       # 🔥 FIX
            cap = _["play_10"].format(details["title"], details["duration_min"])
            streamtype = "youtube"

        else:
            return await mystic.edit_text(_["play_3"])

    else:
        if len(message.command) < 2:
            return await mystic.edit_text(
                _["play_18"],
                reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)),
            )

        slider = True
        query = message.text.split(None, 1)[1].replace("-v", "")
        details, track_id = await YouTube.track(query)
        img = await get_thumb(track_id)           # 🔥 FIX
        cap = _["play_10"].format(details["title"], details["duration_min"])
        streamtype = "youtube"

    # ================= STREAM =================

    if str(playmode) == "Direct":
        await stream(
            _,
            mystic,
            user_id,
            details,
            chat_id,
            user_name,
            message.chat.id,
            video=video,
            streamtype=streamtype,
            spotify=spotify,
            forceplay=fplay,
        )
        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)

    # ================= INLINE BUTTON MESSAGE =================

    buttons = track_markup(
        _,
        track_id,
        user_id,
        "c" if channel else "g",
        "f" if fplay else "d",
    )

    await mystic.delete()
    await message.reply_photo(
        photo=img,        # 🔥 CUSTOM THUMBNAIL
        caption=cap,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

    return await play_logs(message, streamtype="youtube")


# ================= SLIDER CALLBACK (UNCHANGED) =================
# ❗ यहाँ local file allowed नहीं, इसलिए original thumbnail ही रहेगा
