from KaizuryuBot import telethn
from telethon import events, Button, types
from telethon.tl.functions.messages import EditInlineBotMessageRequest
import shortuuid
from KaizuryuBot.modules.sql import whisper_sql
import asyncio

@telethn.on(events.InlineQuery)
async def mainwhisper(event):
    builder = event.builder
    if not event.text:
        return await event.answer(switch_pm='Give me a username or ID!', switch_pm_param='ghelp_whisper')
    text = event.text.split(' ')
    user = text[0]
    first = True
    if not user.startswith('@') and not user.isdigit():
        user = text[-1]
        first = False
        if not user.startswith('@') and not user.isdigit():
            return await event.answer(switch_pm='Give me a username or ID!', switch_pm_param='ghelp_whisper')
    if user.isdigit():
        try:
            chat = await telethn.get_entity(int(user))
            user = f"@{chat.username}" if chat.username else chat.first_name
        except:
            user = user
    message = ' '.join(text[1:]) if first else ' '.join(text[:1])
    if len(message) > 200:
        return await event.answer(switch_pm='Only text upto 200 characters is allowed!', switch_pm_param='ghelp_whisper')
    answers = [
        builder.article(
            f'🤫 Send a whisper message to {user}!',
            description='Only they can see it!',
            text='Generating Whisper message...',
            buttons=Button.inline('🤫 Show Whisper', 'huehue'),
        )
    ]
    await event.answer(answers)

@telethn.on(events.Raw(types.UpdateBotInlineSend))
async def handler(update):
    if not update.query:
        return
    text = update.query.split(' ')
    user = text[0]
    first = True
    if not user.startswith('@') and not user.isdigit():
        user = text[-1]
        first = False
    if first:
        message = ' '.join(text[1:])
    else:
        text.pop()
        message = ' '.join(text)
    if len(message) > 200:
        return
    usertype = 'username'
    whisperType = 'inline'
    if user.startswith('@'):
        usertype = 'username'
    elif user.isdigit():
        usertype = 'id'
    if user.isdigit():
        try:
            chat = await telethn.get_entity(int(user))
            username = f"@{chat.username}" if chat.username else f"**{chat.first_name}**"
        except:
            username = f"`{user}`"
    else:
        username = user
    whisperData = {'user': update.user_id, 'withuser': user, 'usertype': usertype, 'type': whisperType, 'message': message}
    whisperId = shortuuid.uuid()
    whisper_sql.add_whisper(WhisperId=whisperId, WhisperData=whisperData)
    markup = telethn.build_reply_markup([
        [Button.inline('🤫 Show Whisper', f'whisper_{whisperId}')]
    ])
    return await telethn(EditInlineBotMessageRequest(update.msg_id, message=f"A Whisper message for {username}.\nOnly they can read it!", reply_markup=markup))

@telethn.on(events.CallbackQuery(func=lambda event: event.data.decode().startswith('whisper_')))
async def showWhisper(event):
    whisperId = event.data.decode().split('_')[-1]
    whisper =  whisper_sql.get_whisper(whisperId)
    if not whisper:
        return await event.edit("This whisper is not valid anymore!")
    userType = whisper['usertype']
    if event.sender_id == whisper['user']:
        return await event.answer(whisper['message'], alert=True)
    if userType == 'username' and event.sender.username.lower() == whisper[
        'withuser'
    ].replace('@', '').lower():
        await event.answer(whisper['message'], alert=True)
        whisper_sql.del_whisper(whisperId)
        return await event.edit(f"{whisper['withuser']} read the Whisper.")
    elif userType == 'id' and event.sender_id == int(whisper['withuser']):
        user = await telethn.get_entity(int(whisper['withuser']))
        username = user.username or user.first_name
        await event.answer(whisper['message'], alert=True)
        whisper_sql.del_whisper(whisperId)
        return await event.edit(f"{username} read the whisper.")
    else:
        await event.answer("Not your Whisper!", alert=True)


__mod_name__="Whisper"

__help__ = """
*──「 Whisper 」──*
This is how Inline Whisper feature works:
✮ `@Kakashi_ultrabot your message @username OR UserID`
                            OR
✮ `@Kakashi_ultrabot @username OR UserID your message`
"""
