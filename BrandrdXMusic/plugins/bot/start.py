import time
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from youtubesearchpython.future import VideosSearch

import config
from config import BANNED_USERS

from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from strings import get_string


# ================= PRIVATE START ================= #
@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    try:
        await add_served_user(message.from_user.id)

        if len(message.text.split()) > 1:
            name = message.text.split(None, 1)[1]

            # HELP
            if name.startswith("help"):
                return await message.reply_video(
                    video=config.START_VID_URL,
                    caption=_["help_1"].format(config.SUPPORT_CHAT),
                    reply_markup=InlineKeyboardMarkup(help_pannel(_)),
                )

            # SUDO
            if name.startswith("sud"):
                return await sudoers_list(
                    client=client, message=message, _=_
                )

            # INFO
            if name.startswith("inf"):
                msg = await message.reply_text("🔎 Searching...")
                query = name.replace("info_", "", 1)
                query = f"https://www.youtube.com/watch?v={query}"

                results = VideosSearch(query, limit=1)
                data = await results.next()

                if not data["result"]:
                    return await msg.edit_text("❌ No result found.")

                r = data["result"][0]

                caption = _["start_6"].format(
                    r["title"],
                    r["duration"],
                    r["viewCount"]["short"],
                    r["publishedTime"],
                    r["channel"]["link"],
                    r["channel"]["name"],
                    app.mention,
                )

                buttons = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(_["S_B_8"], url=r["link"]),
                            InlineKeyboardButton(_["S_B_9"], url=config.SUPPORT_CHAT),
                        ]
                    ]
                )

                await msg.delete()
                return await app.send_photo(
                    chat_id=message.chat.id,
                    photo=r["thumbnails"][0]["url"].split("?")[0],
                    caption=caption,
                    reply_markup=buttons,
                )

        # NORMAL START
        await message.reply_video(
            video=config.START_VID_URL,
            caption=_["start_2"].format(
                message.from_user.mention, app.mention
            ),
            reply_markup=InlineKeyboardMarkup(private_panel(_)),
        )

    except Exception as e:
        print(f"[START_PM ERROR] {e}")


# ================= GROUP START ================= #
@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    try:
        uptime = int(time.time() - _boot_)

        await message.reply_video(
            video=config.START_VID_URL,
            caption=_["start_1"].format(
                app.mention, get_readable_time(uptime)
            ),
            reply_markup=InlineKeyboardMarkup(start_panel(_)),
        )

        await add_served_chat(message.chat.id)

    except Exception as e:
        print(f"[START_GP ERROR] {e}")


# ================= WELCOME ================= #
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        for member in message.new_chat_members:
            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)
                continue

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                await message.reply_video(
                    video=config.START_VID_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(start_panel(_)),
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

    except Exception as e:
        print(f"[WELCOME ERROR] {e}")
