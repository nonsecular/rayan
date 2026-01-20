import os
from random import randint
from typing import Union
import asyncio

from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BrandrdXMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import db
from BrandrdXMusic.utils.database import is_active_chat, add_active_video_chat
from BrandrdXMusic.utils.exceptions import AssistantErr
from BrandrdXMusic.utils.inline import (
    aq_markup,
    close_markup,
    stream_markup,   # ✅ only this
)
from BrandrdXMusic.utils.stream.queue import put_queue, put_queue_index
from BrandrdXMusic.utils.thumbnails import get_thumb   # ✅ PIL thumbnail
from BrandrdXMusic.utils.pastebin import HottyBin


async def stream(
    _,
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return

    if forceplay:
        await Hotty.force_stop_stream(chat_id)

    # ================= PLAYLIST =================
    if streamtype == "playlist":
        msg = f"{_['play_19']}\n\n"
        count = 0

        for search in result:
            if count == config.PLAYLIST_FETCH_LIMIT:
                break
            try:
                title, duration_min, duration_sec, _, vidid = await YouTube.details(
                    search, False if spotify else True
                )
            except:
                continue

            if not duration_min or duration_sec > config.DURATION_LIMIT:
                continue

            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}. {title[:70]}\n{_['play_20']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []

                file_path, direct = await YouTube.download(
                    vidid, mystic, video=True if video else None, videoid=True
                )

                await Hotty.join_call(
                    chat_id,
                    original_chat_id,
                    file_path,
                    video=True if video else None,
                )

                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )

                img = await get_thumb(vidid)
                button = stream_markup(_, vidid, chat_id)

                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{vidid}",
                        title[:18],
                        duration_min,
                        user_name,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )

                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

        if count == 0:
            return

        link = await HottyBin(msg)
        upl = close_markup(_)

        return await app.send_photo(
            original_chat_id,
            photo=link,
            caption=_["play_21"],
            reply_markup=upl,
        )

    # ================= YOUTUBE =================
    elif streamtype == "youtube":
        vidid = result["vidid"]
        title = result["title"].title()
        duration_min = result["duration_min"]
        status = True if video else None

        file_path, direct = await YouTube.download(
            vidid, mystic, videoid=True, video=status
        )

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )

            img = await get_thumb(vidid)
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)

            await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["queue_4"].format(
                    position, title[:18], duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
        else:
            if not forceplay:
                db[chat_id] = []

            await Hotty.join_call(
                chat_id,
                original_chat_id,
                file_path,
                video=status,
            )

            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )

            img = await get_thumb(vidid)
            button = stream_markup(_, vidid, chat_id)

            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    title[:18],
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )

            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    # ================= SOUNDCLOUD =================
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
            )
        else:
            if not forceplay:
                db[chat_id] = []

            await Hotty.join_call(chat_id, original_chat_id, file_path)

            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
            )

            run = await app.send_photo(
                original_chat_id,
                photo=config.SOUNCLOUD_IMG_URL,
                caption=_["stream_1"].format(
                    config.SUPPORT_CHAT, title[:23], duration_min, user_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    stream_markup(_, chat_id)
                ),
            )

            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
