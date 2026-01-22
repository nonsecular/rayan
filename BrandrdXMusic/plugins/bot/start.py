import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# ───────────────────── PRIVATE START ─────────────────────
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react("❤")

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        # HELP
        if name.startswith("help"):
            await message.reply_sticker(
                "CAACAgUAAxkBAAEQI1RlTLnRAy4h9lOS6jgS5FYsQoruOAAC1gMAAg6ryVcldUr_lhPexzME"
            )
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=help_pannel(_),
            )

        # SUDO LIST
        if name.startswith("sud"):
            await sudoers_list(client, message, _)
            if await is_on_off(2):
                await app.send_message(
                    config.LOGGER_ID,
                    f"{message.from_user.mention} checked **sudo list**\n\n"
                    f"ID: `{message.from_user.id}`\n"
                    f"Username: @{message.from_user.username}",
                )
            return

        # TRACK INFO
        if name.startswith("inf"):
            query = name.replace("info_", "", 1)
            search = VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1)
            result = (await search.next())["result"][0]

            text = _["start_6"].format(
                result["title"],
                result["duration"],
                result["viewCount"]["short"],
                result["publishedTime"],
                result["channel"]["link"],
                result["channel"]["name"],
                app.mention,
            )

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(_["S_B_8"], url=result["link"]),
                        InlineKeyboardButton(_["S_B_9"], url=config.SUPPORT_CHAT),
                    ]
                ]
            )

            await app.send_photo(
                message.chat.id,
                photo=result["thumbnails"][0]["url"].split("?")[0],
                caption=text,
                reply_markup=buttons,
            )
            return

    # NORMAL START (NO ANIMATION)
    out = private_panel(_)

    photo = "assets/nodp.png"
    if message.chat.photo:
        photo = await app.download_media(message.chat.photo.big_file_id)

    await message.reply_photo(
        photo=photo,
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )

    if await is_on_off(config.LOG):
        await app.send_message(
            config.LOG_GROUP_ID,
            f"{message.from_user.mention} started the bot\n\n"
            f"ID: `{message.from_user.id}`\n"
            f"Name: {message.from_user.first_name}",
        )


# ───────────────────── GROUP START ─────────────────────
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(start_panel(_)),
    )
    await add_served_chat(message.chat.id)


# ───────────────────── BOT JOIN WELCOME ─────────────────────
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            lang = await get_lang(message.chat.id)
            _ = get_string(lang)

            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)
                return

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

                await message.reply_photo(
                    photo=config.START_IMG_URL,
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
            print(e)
