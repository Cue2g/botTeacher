from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from controllers.user import users
import io
import speech_recognition as sr
from pydub import AudioSegment

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userId = update.effective_user.id
    user = users.find_user(user_id=userId)
    if user is None:
        users.create_user(
            userId,
            update.effective_user.first_name,
            update._effective_user.last_name,
            update.effective_user.username,
            None,
            None   
        )        
    data = [
        [InlineKeyboardButton("SPA 🇪🇦", callback_data='Spanish')],
        [InlineKeyboardButton("ENG 🇺🇸", callback_data='English')],
        [InlineKeyboardButton("ITA 🇮🇹", callback_data='Italian')],
    ]
    reply_markup = InlineKeyboardMarkup(data)
    await update.message.reply_text('Por favor seleccione el idioma que quiere aprender', reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    selected_language = query.data
    user_id = update.effective_user.id
    await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    updateLeng = users.update_lang(user_id,selected_language)
    if updateLeng == None:
        await query.answer(text=f"Hubo un error a la hora de cambiar el lenguaje")
    await query.answer(text=f"Has seleccionado el idioma: {selected_language}")

async def handle_audio(update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.voice:
        buffer = io.BytesIO()
        voice_file_id = message.voice.file_id
        voice_file = await context.bot.get_file(voice_file_id)
        await voice_file.download_to_memory(buffer)
        recognizer = sr.Recognizer()

        audio = AudioSegment.from_ogg(io.BytesIO(buffer.getvalue()))
        wav_data = audio.export(format="wav").read()

        try:
            with sr.AudioFile(io.BytesIO(wav_data)) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="en-EN")
            await update.message.reply_text(text)
        except sr.UnknownValueError:
            await update.message.reply_text('No se puedo reconocer')