import buttons
from config import TOKEN
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('*Приветственное сообщение*', reply_markup=buttons.main_menu)
    await message.answer("""Вы можете ознакомиться с тарифами нажав на кнопку «Тарифы» и подобрать для себя  подходящий, гарантируем, что вы не пожалеете 🚀\n
Будем рады видеть вас у себя в команде! 🤝\n
Если у вас возникли вопросы, обратитесь к менеджеру👇\n@username
                            """, reply_markup=buttons.tarif)


@dp.message_handler(Text('Тарифы 🚀'))
async def tarifs_reply(message: types.Message):
    await message.answer('Тарифы', reply_markup=buttons.tarifs)


@dp.callback_query_handler(lambda c: c.data == 'tarif')
async def tarifs(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.from_user.id, 'Тарифы', reply_markup=buttons.tarifs)


@dp.message_handler(Text('Мой тариф ⏳'))
async def my_tarif(message: types.Message):
    tar = None
    await message.anser(f'Ваш тариф: {tar}')


@dp.message_handler(Text('Отзывы 📖'))
async def answers(message: types.Message):
    link  =  'link'
    await message.anser(f'Канал с отзывами: {link}')


@dp.message_handler(Text('Обучающие курсы 👨‍💻'))
async def kurs(message: types.Message):
    await message.anwser(f'Для получения доступа к курсам нужно обладать подпиской 2 или 3 уровня')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)