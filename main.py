from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters,CommandHandler,CallbackQueryHandler
from dotenv import load_dotenv
from mongo import DBConnection
from cmds import start,button_callback,handle_audio
from controllers.openai import openAI
import os




load_dotenv()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    openAI.do_request()
    await update.message.reply_text('test')
    
def main() -> None:
    BOT_KEY = os.environ.get("API_BOT_KEY", "INSERT_BOT_KEY_HERE")
    DBConnection()
    application = ApplicationBuilder().token(BOT_KEY).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test",test))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.VOICE  ,handle_audio))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    