from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')


# функция-обработчик команды /start
async def start(update, context):
    await update.message.reply_text("Добро пожаловать, мой дорогой друг!")


# функция-обработчик команды /help
async def help(update, context):
    await update.message.reply_text("Этот бот предназначен для обучения! ❗")


# функция-обработчик текстовых сообщений
async def text(update, context):
    await update.message.reply_text("Текст, текст, текст…")


# функция-обработчик сообщений с изображениями
async def image(update, context):
    await update.message.reply_text("Мы получили от тебя фотографию!")


# функция-обработчик голосовых сообщений
async def voice(update, context):
    await update.message.reply_text("Мы получили от тебя голосовое соообщение!")


def main():

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик команды /help
    application.add_handler(CommandHandler("help", help))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с фотографиями
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # запускаем бота (нажать Ctrl-C для остановки бота)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()