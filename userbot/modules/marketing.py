from time import sleep

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, owner
from userbot.utils import edit_or_reply, man_cmd

@man_cmd(pattern="jasa(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Jasa Pasang Ubot?Filesharing?Musik?tpi lu gamau ribet,Ini dia solusinya**")
    sleep(5)
    await xx.edit("**@Jowo_Store Jasa Pasang Ubot dll terpercaya klo ga percaya tanya aja sama pak haji**")


@man_cmd(pattern=r"js(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**The Js-Userbot,Jasa Pemasangan Userbot Terpercaya & Diverifikasi Oleh The Js!!\nJoin @Jowo_Store**"
    )
    sleep(59)
    await xx.edit("@Jowo_Store")


CMD_HELP.update(
    {
        "marketing": f"**Plugin : **`marketing`\
        \n\n  •  **Syntax :** `{cmd}jasa`\
        \n  •  **Syntax  :** `{cmd}js`\
        \n  •  **Function : liat sendiri**\
    "
    }
)

