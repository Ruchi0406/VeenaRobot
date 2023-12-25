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

    meme = await drawText(file, text)

    await bot.send_file(event.chat_id, file=meme, force_document=False)

    await msg.delete()

    os.remove(meme)


async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)

    i_width, i_height = img.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./MukeshRobot/resources/default.ttf"

    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)

    current_h, pad = 10, 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = m_font.getsize(u_text)

            draw_text_position = (
                ((i_width - u_width) / 2),
                int((current_h / 640) * i_width),
            )

            draw.text(
                xy=draw_text_position,
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(draw_text_position[0] + 2, draw_text_position[1]),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = m_font.getsize(l_text)

            draw_text_position = (
                ((i_width - u_width) / 2),
                i_height - u_height - int((20 / 640) * i_width),
            )

            draw.text(
                xy=draw_text_position,
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(draw_text_position[0] + 2, draw_text_position[1]),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(image_name)
    img.save(webp_file, "webp")

    return webp_file


__mod_name__ = "ᴍᴍғ"
__help__ = """ 
⫸ /mmf <ᴛᴇxᴛ> ◉ ᴛᴏ ᴍᴇᴍɪғʏ
"""
