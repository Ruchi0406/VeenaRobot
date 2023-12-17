from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image, ImageDraw, ImageFont
import os

# Function to handle the /mmf command
def memify(update: Update, context: CallbackContext) -> None:
    # Check if the message contains a photo or sticker
    if update.message.photo or update.message.sticker:
        # Determine the file ID based on the content type
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
        else:  # If it's a sticker
            file_id = update.message.sticker.file_id

        # Download the file
        file = context.bot.get_file(file_id)
        file.download('input_file')

        # Open the file using PIL
        image = Image.open('input_file')

        # Add text to the image
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), "Memified by Veena Music", font=font, fill="white")

        # Save the memified image
        image.save('output_meme.jpg')

        # Send the memified image back to the user
        context.bot.send_photo(update.message.chat_id, photo=open('output_meme.jpg', 'rb'))

        # Clean up temporary files
        os.remove('input_file')
        os.remove('output_meme.jpg')
    else:
        update.message.reply_text("Please send a photo or sticker to memify!")

# Set up the bot with the token from environment variable
updater = Updater(os.getenv("TOKEN"))

# Set up command handlers
updater.dispatcher.add_handler(CommandHandler("mmf", memify))

# Start the bot
updater.start_polling()
updater.idle()
