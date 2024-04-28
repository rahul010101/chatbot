from typing import Final
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pdfkit
from urllib.parse import urlparse, parse_qs

TOKEN: Final = 'YOUR_BOT_TOKEN'
BOT_USERNAME: Final = '@rahulnai_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a new chatbot!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''You can type /start or /help or /link''')

def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'i love python' in processed:
        return 'Remember to subscribe!'
    return 'I do not understand what you wrote...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
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
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Errors
    app.add_error_handler(error)
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
