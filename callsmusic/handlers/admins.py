from asyncio import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message

from .. import queues
from ..callsmusic import callsmusic
from ..helpers.chat_id import get_chat_id
from ..helpers.decorators import authorized_users_only
from ..helpers.decorators import errors
from ..helpers.filters import command
from ..helpers.filters import other_filters


@Client.on_message(command('pause') & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    (
        await message.reply_text('<b>⏸ Music di berhentikan 👉😁👈...</b>', False)
    ) if (
        callsmusic.pause(get_chat_id(message.chat))
    ) else (
        await message.reply_text('<b>❌ Tidak ada yg di play anjing 👉😁👈...</b>', False)
    )


@Client.on_message(command('resume') & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    (
        await message.reply_text('<b>▶️ Di putar lagi..</b>', False)
    ) if (
        callsmusic.resume(get_chat_id(message.chat))
    ) else (
        await message.reply_text('<b>❌ Tidak ada yg di berhentikan</b>', False)
    )


@Client.on_message(command('stop') & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text('<b>❌ Tidak ada lagu yang di play</b>', False)
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass
        await callsmusic.stop(chat_id)
        await message.reply_text('<b>⏹ Stopped streaming</b>', False)


@Client.on_message(command('skip') & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text('<b>❌ Tidak ada yang di putar..</b>', False)
    else:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await callsmusic.stop(chat_id)
        else:
            await callsmusic.set_stream(
                chat_id,
                queues.get(chat_id)['file'],
            )
        await message.reply_text('<b>✅ Anjing laguan kok dikit-dikit skip.</b>', False)


@Client.on_message(command('mute') & other_filters)
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = callsmusic.mute(get_chat_id(message.chat))
    (
        await message.reply_text('<b>✅ Bisu</b>', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('<b>❌ Kasian di muted anjing 👉😁👈..</b>', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('<b>❌ Tidak ada yang menelpon...</b>', False)
    )


@Client.on_message(command('unmute') & other_filters)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(get_chat_id(message.chat))
    (
        await message.reply_text('<b>✅ Goblog di buka bisu nya</b>', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('<b>❌ Tidak Bisu</b>', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('<b>❌ Tidak menerima telpon..</b>', False)
    )
