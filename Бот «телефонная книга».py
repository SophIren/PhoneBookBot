from telegram.ext import Updater, MessageHandler, Filters
import phone


def message_handler(bot, update):
    message = update.message.text.split()

    message_length = len(message)
    if message_length == 1:
        phone_ = phone.get_formatted_phone_number(message[0])
        name = phone_book.get_name(phone_)
        update.message.reply_text(name)
    elif message_length == 2:
        name = message[0] + ' ' + message[1]
        phone_ = phone_book.get_phone(name)
        update.message.reply_text(phone_)
    elif message_length == 3:
        name = message[0] + ' ' + message[1][:-1]
        phone_ = phone.get_formatted_phone_number(message[2])
        if len(phone_) == 11:
            phone_book.add_writing(phone_, name)
            update.message.reply_text("Запись успешно добавлена (изменена)!")
            phone_book.save_data()
        else:
            update.message.reply_text("Не понял запроса :(")
    else:
        update.message.reply_text("Не понял запроса :(")


phone_book = phone.PhoneBook(1000)
phone_book.load_names_data("russian_names.json")
phone_book.load_surnames_data("russian_surnames.json")
phone_book.generate_data()
phone_book.save_data("phones.json")

updater = Updater("719002995:AAHJ0LmpAwuaiix7rHFz_ZsUonF0KhbT5M0")
dp = updater.dispatcher

text_handler = MessageHandler(Filters.text, message_handler)
dp.add_handler(text_handler)

updater.start_polling()
updater.idle()
