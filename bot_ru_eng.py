from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, ReplyKeyboardMarkup
from pprint import pprint
from dotenv import load_dotenv
import os

# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

lang = None

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
        txt_ans = "Вы нажали на кнопку: "
    elif lang == "eng":
        txt_ans = "You pressed the button: "

    await query.edit_message_text(text=txt_ans + query.data)


# функция-обработчик текстовых сообщений
async def text(update: Update, _):
    global lang

    if lang == "rus":
        txt_ans = "Текстовое сообщение получено!"
    elif lang == "eng":
        txt_ans = "We’ve received a message from you!"

    await update.message.reply_text(txt_ans)


# функция-обработчик сообщений с изображениями
async def image(update: Update, _):

    # получаем изображение из апдейта: 0 - низкое кач-во, 1 - среднее, 2 (-1) - высокое
    file = await update.message.photo[-1].get_file()

    # сохраняем изображение на диск
    await file.download_to_drive("photos/image.jpg")

    global lang

    if lang == "rus":
        txt_ans = "Фотография сохранена"
    elif lang == "eng":
        txt_ans = "Photo saved!"

    await update.message.reply_text(txt_ans)


# функция-обработчик голосовых сообщений
async def voice(update: Update, _):
    global lang

    if lang == "rus":
        txt_ans = "Голосовое сообщение получено!"
    elif lang == "eng":
        txt_ans = "We’ve received a voice message from you!"

    # Отправка изображения с подписью
    await update.message.reply_photo(photo=open("images/bot_image.jpg", 'rb'), caption=txt_ans)


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
