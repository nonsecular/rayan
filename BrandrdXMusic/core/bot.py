from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class Hotty(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="BrandrdXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = f"{self.me.first_name} {(self.me.last_name or '')}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        if not config.LOGGER_ID:
            LOGGER(__name__).info("LOGGER_ID not set.")
            return

        try:
            await self.send_message(
                config.LOGGER_ID,
                (
                    f"<b>🤖 Bot Started</b>\n\n"
                    f"• ID: <code>{self.id}</code>\n"
                    f"• Name: {self.name}\n"
                    f"• Username: @{self.username}"
                ),
                parse_mode="html",
            )

            try:
                member = await self.get_chat_member(config.LOGGER_ID, self.id)
                if member.status not in (
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.OWNER,
                ):
                    LOGGER(__name__).warning(
                        "Bot is not admin in LOGGER group/channel."
                    )
            except Exception:
                pass

        except errors.ChatWriteForbidden:
            LOGGER(__name__).warning("No permission to write in LOGGER group.")

        except errors.PeerIdInvalid:
            LOGGER(__name__).warning("LOGGER_ID invalid.")

        except errors.ChannelInvalid:
            LOGGER(__name__).warning("Bot not added to LOGGER channel.")

        except Exception as e:
            LOGGER(__name__).error(f"Logger error: {e}")

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
