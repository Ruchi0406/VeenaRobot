import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from MukeshRobot import telethn as bot
from MukeshRobot.events import register

Credit = "Aditya"

@register(pattern="^/mmf ?(.*)")
async def handler(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Provide Some Text To Draw!")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("```Reply to an image/sticker.```")
        return
    file = await bot.download_media(reply_message)
    msg = await event.reply("```Memifying this image! ✊🏻 ```")
    if "Aditya" in Credit:
        pass
    else:
        await event.reply("This nigga removed credit line from code")
    text = str(event.pattern_match.group(1)).strip()
    if len(text) < 1:
        return await msg.reply("You might want to try `/mmf text`")
    meme = await drawText(draw=ImageDraw.Draw(file), position=((0, 0)), font_size=12, image_path=file, text=text)
    await bot.send_file(event.chat_id, file=meme, force_document=False)
    await msg.delete()
    os.remove(meme)


async def drawText(draw, position, font_size, image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    if os.name == "nt":
        fnt = "ariel.ttf"
    else:
        fnt = "./MukeshRobot/resources/default.ttf"
    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))
    # Rest of the code remains unchanged...
    # ...

__mod_name__ = "Mᴍғ"
__help__ = """
⫸ /mmf <ᴛᴇxᴛ> ◉ ᴛᴏ ᴍᴇᴍɪғʏ
"""
