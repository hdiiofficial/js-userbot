import asyncio
from datetime import datetime
from io import BytesIO

from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import Channel

import userbot.modules.sql_helper.gban_sql as gban_sql
from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, DEVS, bot
from userbot.events import register
from userbot.utils import edit_or_reply, get_user_from_event, man_cmd

from .admin import BANNED_RIGHTS, UNBAN_RIGHTS


@register(incoming=True, from_users=DEVS, pattern=r"^\.cgban(?: |$)(.*)")
async def cgban(event):
    if event.fwd_from:
        return
    gbun = await edit_or_reply(event, "`MengGbanned...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, gbun)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gbun.edit("**Ngapain NgeGban diri sendiri Goblok 🐽**")
        return
    if user.id in DEVS:
        await gbun.edit("**Gagal GBAN karena dia adalah Pembuat saya 🗿**")
        return
    if gban_sql.is_gbanned(user.id):
        await gbun.edit(
            f"**Si** [Jamet](tg://user?id={user.id}) **ini sudah ada di daftar gbanned**"
        )
    else:
        gban_sql.freakgban(user.id, reason)
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await gbun.edit("**Anda Tidak mempunyai GC yang anda admin 🥺**")
        return
    await gbun.edit(
        f"**initiating gban of the** [Jamet](tg://user?id={user.id}) **in** `{len(san)}` **groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda tidak memiliki izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gbun.edit(
            f"**GBanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Reason :** `{reason}`"
        )
    else:
        await gbun.edit(
            f"**GBanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Added to gbanlist.**"
        )

@register(incoming=True, from_users=DEVS, pattern=r"^\.cungban(?: |$)(.*)")
async def cungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "`UnGbanning...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.freakungban(user.id)
    else:
        await ungbun.edit(
            f"**Si** [Jamet](tg://user?id={user.id}) **ini tidak ada dalam daftar gban Anda**"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await ungbun.edit("**Anda Tidak mempunyai GC yang anda admin 🥺**")
        return
    await ungbun.edit(
        f"**initiating ungban of the** [Jamet](tg://user?id={user.id}) **in** `{len(san)}` **groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda tidak memiliki izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"**Ungbanned** [{user.first_name}](tg://user?id={user.id}`) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Reason :** `{reason}`"
        )
    else:
        await ungbun.edit(
            f"**Ungbanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Removed from gbanlist**"
        )


CMD_HELP.update(
    {
        "cgban": f"**plugin :**`cgban`\
        \n\n• Syntax :**`{cmd}cgban <username/userid>`\
        \n\n• Syntax :**`{cmd}cungban <username/userid>`\
    "
    }
)
