from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

tarif = InlineKeyboardMarkup()
menu_tarifs = InlineKeyboardButton('Тарифы', callback_data='tarif')
tarif.add(menu_tarifs)

tarifs = InlineKeyboardMarkup()
tarif_1 = InlineKeyboardButton('Неделя (1 ур.) - 150₽ 🦋', callback_data='tarif_1')
tarif_2 = InlineKeyboardButton('Месяц (2 ур.) - 500₽ 😇', callback_data='tarif_2')
tarif_3 = InlineKeyboardButton('Год (3 ур.) - 1500₽ 🤑', callback_data='tarif_3')
tarifs.add(tarif_1).add(tarif_2).add(tarif_3)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
tarif_and_my = ['Тарифы 🚀', 'Мой тариф ⏳']
ans = KeyboardButton('Отзывы 📖')
kurs = KeyboardButton('Обучающие курсы 👨‍💻')
main_menu.add(*tarif_and_my).add(kurs).add(ans)
