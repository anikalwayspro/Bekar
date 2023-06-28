from platform import python_version as y
from telegram import __version__ as o
from pyrogram import __version__ as z
from telethon import __version__ as s
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from KaizuryuBot import pgram as client, dispatcher, OWNER_USERNAME


Kaizuryu = "https://telegra.ph/file/46db0982ecbe5a1e2bffe.jpg"


@client.on_message(filters.command(["repo", "source"]))
async def repo(client, message):
    await message.reply_photo(
        photo=Kaizuryu,
        caption=f"""**ʜᴇʏ​ {message.from_user.mention()},\n\nɪ ᴀᴍ [{dispatcher.bot.first_name}](t.me/{dispatcher.bot.username})**

**» ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ​ :** @{OWNER_USERNAME}
**» ᴩʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{y()}`
**» ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{o}` 
**» ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{s}` 
**» ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{z}`

**{dispatcher.bot.username} If You Want Repo Of This Bot Please Contact To My Owner**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "• Owner •", url=f"https://t.me/{OWNER_USERNAME}"
                    ),
                    InlineKeyboardButton(
                        "• Support •",
                        url="https://t.me/Samurai_botsupport",
                    ),
                ]
            ]
        ),
    )


__mod_name__ = "Rᴇᴩᴏ"
