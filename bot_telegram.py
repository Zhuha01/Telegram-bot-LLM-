import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from other import is_cyrillic
from agent import agent

start_message = """
Hello! 👋 I'm your personal cybersecurity assistant 🔐.

What can I do? Here's my arsenal:
✨ Answer your questions about cybersecurity.
✨ Explain how to use popular encryption methods:
• Vigenere cipher
• Atbash cipher
• Trithemium cipher
• Daniel Defoe cipher
• Caesar cipher
✨ Encrypt and decrypt messages using these methods.

📌 *How to work with me?*
To encode or decode a message, write the text in quotes, and the key or step (if necessary) in the format:
`key = "here is the key or step".

📌 *Example request:*
Encrypt me the message "Hello, my name is Maxim" using the Vigenere method with key = "Mom"

Ready to make your message secure! Write - and I'll organize everything 🛡️🤖

It's better to write me a message in English, for more correct and streamlined work.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if is_cyrillic(text):
        await update.message.reply_text(
            "Дякую, що пишеш українською! Але для найкращої роботи бота, пишіть краще англійською 🙂")
        return
    try:
        response = agent.run(text)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Sorry, something went wrong.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_message)


app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("Бот запущений...")
app.run_polling()