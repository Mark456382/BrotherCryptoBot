import time
import buttons
import messages as mg
from base.ORM import BrotherCryptoBot
from threading import Thread
from config import TOKEN, PAY_TOKEN
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as md
import aioschedule


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)
db = BrotherCryptoBot()


# class Mess(StateGroup):
#     text = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if db.check_user(message.from_user.id) == []:
        db.add_user(user_id=message.from_user.id)
        await message.answer('*Приветственное сообщение*',
                        reply_markup=buttons.main_menu)
        await message.answer(
        """Вы можете ознакомиться с тарифами нажав на кнопку «Тарифы» и подобрать для себя  подходящий, гарантируем, что вы не пожалеете 🚀\n
Будем рады видеть вас у себя в команде! 🤝\n
Если у вас возникли вопросы, обратитесь к менеджеру👇\n@username
                                """, reply_markup=buttons.tarif)
    else:
        await message.answer('С возвращением!!!', reply_markup=buttons.main_menu)

# -------------------------- Тарифы -------------------------------------
@dp.message_handler(Text('Тарифы 🚀'))
async def tarifs_reply(message: types.Message):
    await message.answer('Тарифы', reply_markup=buttons.tarifs)


@dp.callback_query_handler(lambda c: c.data == 'tarif')
async def tarifs(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.send_message(callback.from_user.id,
                        'Тарифы',
                        reply_markup=buttons.tarifs)


@dp.callback_query_handler(lambda c: c.data == 'level_1')
async def level_1(callback: types.CallbackQuery):
    PRICE = types.LabeledPrice(label='Тариф: Неделя (1 ур.) - 150₽ 🦋', amount=15000)
    if PAY_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback.from_user.id, "Тестовый платеж!!!")

    await bot.send_invoice(callback.from_user.id,
                        title="Тариф: Неделя (1 ур.) - 150₽ 🦋",
                        description="Активация подписки на бота на 1 неделю",
                        provider_token=PAY_TOKEN,
                        currency="rub",
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="test-invoice-payload")


@dp.callback_query_handler(lambda c: c.data == 'level_2')
async def level_2(callback: types.CallbackQuery):
    PRICE = types.LabeledPrice(label='Месяц (2 ур.) - 500₽ 😇', amount=50000)
    if PAY_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback.from_user.id, "Тестовый платеж!!!")

    await bot.send_invoice(callback.from_user.id,
                        title="Тариф: Месяц (2 ур.) - 500₽ 😇",
                        description="Активация подписки на бота на 1 месяц",
                        provider_token=PAY_TOKEN,
                        currency="rub",
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="test-invoice-payload")


@dp.callback_query_handler(lambda c: c.data == 'level_3')
async def level_3(callback: types.CallbackQuery):
    PRICE = types.LabeledPrice(label='Год (3 ур.) - 1500₽ 🤑', amount=150000)
    if PAY_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback.from_user.id, "Тестовый платеж!!!")

    await bot.send_invoice(callback.from_user.id,
                        title="Тариф: Год (3 ур.) - 1500₽ 🤑",
                        description="Активация подписки на бота на 1 год",
                        provider_token=PAY_TOKEN,
                        currency="rub",
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="test-invoice-payload")


# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    pay = message.successful_payment.total_amount // 100
    if pay == 150:
        db.set_tarif(user_id=message.from_user.id, tarif=1, time=18)
    elif pay == 500:
        db.set_tarif(user_id=message.from_user.id, tarif=2, time=43200)
    else:
        db.set_tarif(user_id=message.from_user.id, tarif=3, time=482880)
    await bot.send_message(message.chat.id,
                            f"Платеж на сумму {pay} {message.successful_payment.currency} прошел успешно!!!")
# ---------------------------------------------------------------------------


@dp.message_handler(Text('Мой тариф ⏳'))
async def my_tarif(message: types.Message):
    tar = db.get_tarif(user_id=message.from_user.id)
    time = db.get_time(user_id=message.from_user.id)

    if tar != None:
        await message.answer(f'Ваш тариф: {tar} уровня\n{mg.decription[tar]}\nОставшееся время: {time}' if tar != None else 'Вы еще не приобрели тариф') 
    else: await message.answer('Вы ещё не приобрели тариф')

@dp.message_handler(Text('Отзывы 📖'))
async def answers(message: types.Message):
    link = 'отзывы'
    await message.answer(f'Канал с отзывами: @{link}')


@dp.message_handler(Text('Обучающие курсы 👨‍💻'))
async def kurs(message: types.Message):
    tar = db.get_tarif(user_id=message.from_user.id)
    if tar == 1:
        await message.answer('Для получения доступа к курсам нужно обладать подпиской 2 или 3 уровня')
    else:
        await message.answer('Канал с обучающими уроками и курсами - @канал')

@dp.message_handler(commands=['/send_message'])
async def send_message(message: types.Message):
    ...

# @dp.message_handler(state=)
# async def send_mess(message: types.Message):
#     users = db.users_with_tarif()
#     for i in users:
#         await bot.send_message(i[0], text=my_text)


def update_time():
    users = db.get_all_user_id()
    while True:
        for i in users:
            if i[1] != None:
                db.set_time(user_id=i[0], time=i[1]-1)
            else: pass
        time.sleep(1)



if __name__ == '__main__':
    thread = Thread(target=executor.start_polling, args=(dp)).run()
    # executor.start_polling(dp, skip_updates=True)
    thread_1 = Thread(target=update_time, daemon=True)
    thread_1.start()