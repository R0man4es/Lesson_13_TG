from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, ReplyKeyboardMarkup
from pprint import pprint
from dotenv import load_dotenv
import os

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

# INLINE
# форма inline клавиатуры
inline_frame = [[InlineKeyboardButton("Русский", callback_data="rus")],
                [InlineKeyboardButton("English", callback_data="eng")]]
# создаем inline клавиатуру
inline_keyboard = InlineKeyboardMarkup(inline_frame)

# REPLY
# форма reply клавиатуры
reply_frame = [['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Уфа']]
# создаем reply клавиатуру
reply_keyboard = ReplyKeyboardMarkup(reply_frame,
                                     resize_keyboard=True,  # автоматический размер кнопок
                                     one_time_keyboard=True)  # скрыть коавиатуру после нажатия


# функция-обработчик команды /start
async def start(update: Update, _):
    #
    # прикрепляем inline клавиатуру к сообщению
    await update.message.reply_text('Выберите язык общения / Select the language of communication:',
                                    reply_markup=inline_keyboard)


# # функция-обработчик команды /city
# async def city(update: Update, _):
#
#     # прикрепляем reply клавиатуру к сообщению
#     await update.message.reply_text('Пример reply клавиатуры:', reply_markup=reply_keyboard)


# функция-обработчик нажатий на кнопки
async def button(update: Update, _):
    # получаем callback query из update
    query = update.callback_query

    global lang
    lang = query.data

    #   # всплывающее уведомление
    #   await query.answer('Это всплывающее уведомление!')

    # редактируем сообщение после нажатия
    if lang == "rus":
        await query.edit_message_text(text=f"Вы нажали на кнопку: {query.data}")
    else:
        await query.edit_message_text(text=f"You pressed the button: {query.data}")


# функция-обработчик текстовых сообщений
async def text(update: Update, context):

    global lang

    if lang == "rus":
        await update.message.reply_text("Текстовое сообщение получено!")
    else:
        await update.message.reply_text("We’ve received a message from you!")


# функция-обработчик сообщений с изображениями
async def image(update: Update, context):
    await update.message.reply_text("Мы получили от тебя фотографию!")


# функция-обработчик голосовых сообщений
async def voice(update: Update, context):
    await update.message.reply_text("Голосовое сообщение получено")


def main():
    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # # добавляем обработчик команды /city
    # application.add_handler(CommandHandler("city", city))

    # добавляем CallbackQueryHandler (только для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))

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
