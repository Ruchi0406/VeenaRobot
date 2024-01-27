import requests
from PIL import Image
import io
import os
from MukeshRobot import telethn as tbot
from MukeshRobot.events import register

API_URL = "https://api-inference.huggingface.co/models/OEvortex/HelpingAI-PixelCraft"
HEADERS = {"Authorization": "Bearer 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"}

@register(pattern="^/genai(?: (.+))?")
async def generate_image(event):
    if event.fwd_from:
        return

    prompt = event.pattern_match.group(1)

    if prompt:
        # Send "Please wait" message
        processing_message = await event.reply("Please wait, generating image...")

        try:
            # Make a request to GPT API for image generation
            response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

            if response.status_code == 200:
                # Save the generated image
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                image.save('generated_image.jpg')

                # Send the generated image
                with open('generated_image.jpg', 'rb') as img:
                    await event.reply(file=img)
                    print("Image generated")

                # Delete the saved image file after sending it to the user
                image.close()
                os.remove('generated_image.jpg')
            else:
                # If there's an error with the API, inform the user
                await processing_message.edit("Error communicating with Image Generation API.")
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            await processing_message.edit(f"Error: {str(e)}. Please try again later.")
        except Exception as e:
            # Handle unexpected errors
            await processing_message.edit(f"Unexpected error: {str(e)}. Please try again later.")
    else:
        # Provide information about the correct command format
        await event.reply("Please provide a prompt after /imagegen command. For example: `/imagegen Generate a beautiful landscape`")

__mod_name__ = "ImageGenAI"
__help__ = """
/genai :- Genrate images with Ai
 """
