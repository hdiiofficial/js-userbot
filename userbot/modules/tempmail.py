# BASED FROM ULTROID PORTED FOR LYNX USERBOT BY ALVIN / @LIUALVINAS
# THANKS ULTROID
# DONT REMOVE THIS
# credite phoenix ubot
# Recode by @hdiiofficial

from telethon import events
from userbot import CMD_HELP, bot
from userbot import CMD_HANDLER as cmd
from userbot.events import man_cmd
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio


@bot.on(man_cmd(outgoing=True, pattern=r"^\.tm(?: |$)(.*)"))
async def tempmail(event):
    chat = "@TempMailBot"
    jsuser = await event.edit("Sedang Memprosess...")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True,
                from_users=1535645343
            )
            )
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("Generate New")
            response = await response
            jsuserbot = ((response).reply_markup.rows[2].buttons[0].url)
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await jsuser.edit("`Mohon Maaf, Silahkan Buka` @TempMailBot `Lalu Tekan Start dan Coba Lagi.`")
            return
        await event.edit(f"**Ubot TEMPMAIL** ~ `{response.message.message}`\n\n[KLIK DISINI UNTUK VERIFIKASI]({jsuserbot})")



CMD_HELP.update(
    {
        "tempmail": f"**Plugin : **`TempMail`\
        \n\n  •  **Syntax :** `{cmd}tm`\
        \n  •  **Function : **membuat akun sementara dari tempmail.\
    "
    }
)
