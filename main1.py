from typing import Final
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pdfkit
from urllib.parse import urlparse, parse_qs
import pyjokes
import requests

TOKEN: Final = 'YOUR_TELEGRAM_TOKEN'
BOT_USERNAME: Final = '@rahulnai_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    reply_message = f'''Hello, {user_name}\nWelcome to the chatbot!'''
    await update.message.reply_text(reply_message)

'''def generate_joke() -> str:
    joke = pyjokes.get_joke()
    return f"Here's a joke for you:\n{joke}"'''

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://icanhazdadjoke.com/slack"
    response = requests.get(url)
    joke_data = response.json()
    joke_text = joke_data["attachments"][0]["text"]
    await update.message.reply_text(joke_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''You can type:\n/start\n/help\n/link\n/joke\nAnd for normal text you can type:\nhi\nhow are you\nwhat can you do\nhow old are you\nthank you or thanks''')

def handle_response(text: str, user_name: str) -> str:
    processed: str = text.lower()
    if 'hi' in processed:
        return f"Hi, {user_name}!\n"
    if 'how are you' in processed:
        return f"I am doing great, {user_name}! Thank you for asking!"
    if 'what can you do' in processed:
        return f"I can help you with tasks such as converting an webpage in to an pdf and give you a pdf file, {user_name}. You want to try type ' /link https://yourlink.com '"
    if 'how old are you' in processed:
        return f"I am a chatbot, so I don't have an age, {user_name}. But I am always here to assist you!"
    if 'thank you' in processed or 'thanks' in processed:
        return f"Anytime, {user_name}! I'm always here to help!"
    return f"I'm sorry, {user_name}, but I do not understand what you wrote..."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user_name: str = update.message.from_user.first_name
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    response = handle_response(text, user_name)
    
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def save_html_as_pdf(url: str) -> bytes:
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Update with your actual path
    options = {
        'quiet': '',
    }

    try:
        pdf_bytes = pdfkit.from_url(url, False, options=options, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))
        print("PDF generated successfully")
        return pdf_bytes
    except Exception as e:
        print(f"Failed to convert HTML to PDF. Error: {e}")
        return None

async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = " ".join(context.args)
    pdf_bytes = save_html_as_pdf(url)
    if pdf_bytes:
        await update.message.reply_document(document=InputFile(pdf_bytes, filename="output.pdf"))
    else:
        await update.message.reply_text("Failed to generate PDF provide link like this /link 'your link'")

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('link', link_command))
    app.add_handler(CommandHandler('joke', joke_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Errors
    app.add_error_handler(error)
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
