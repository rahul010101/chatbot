import asyncio
import telegram
from telegram.ext import MessageHandler, filters
from google.generativeai import configure, GenerativeModel

# Configure API key
configure(api_key="YOUR_AI_KEY")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = GenerativeModel(model_name="gemini-1.5-pro-latest",
                        generation_config=generation_config,
                        safety_settings=safety_settings)

# Define a function to handle incoming messages
async def message_handler(update):
    if update.message.text:
        user_input = update.message.text
        try:
            convo = model.start_chat(history=[])
            convo.send_message(user_input)
            ai_response = convo.last.text
            await update.message.reply_text(ai_response)  # Await here
        except ValueError as e:
            if str(e) == "content must not be empty":
                print("AI response is empty.")
                # Handle the case where the AI response is empty, you can log the error or send a message to the user informing them about the issue
            else:
                print("An unexpected error occurred:", e)
                # Handle other ValueError exceptions gracefully
        except telegram.error.TimedOut as e:
            print("Telegram API rate limit exceeded:", e)
            # Reply with a message asking the user to try again later
            await update.message.reply_text("Sorry, I'm currently experiencing high traffic. Please try again later.")
        except Exception as e:
            print("An unexpected error occurred:", type(e), e)  # Print the type of exception
            # Handle other unexpected errors gracefully, you can log the error or send a message to the user informing them about the issue
    else:
        # If the message is not text, reply with a message asking the user to resend a text message
        await update.message.reply_text("Sorry, I can only process text messages. Please send a text message.")






async def main():
    # Create a bot instance
    bot = telegram.Bot(token="YOUR_TELEGRAM_TOKEN")

    # Start message polling and register message handler
    last_update_id = None
    while True:
        updates = await bot.get_updates(offset=last_update_id)
        for update in updates:
            if update.message:
                await message_handler(update)
                last_update_id = update.update_id + 1

if __name__ == "__main__":
    asyncio.run(main())
