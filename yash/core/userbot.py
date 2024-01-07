from pyrogram import Client, errors, enums 
import config
from ..logging import LOGGER


class Userbot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Userbot...")
        super().__init__(
            name="user_session",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION,
            in_memory=True,
            no_updates=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOG_CHANNEL,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",parse_mode=enums.ParseMode.HTML
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Userbot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Userbot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()
        LOGGER(__name__).info(f"UserBot Started as {self.name}")

    async def stop(self):
        await super().stop()
