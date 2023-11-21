<p align="center">
      <a href="https://imgur.com/9t3fDgT"><img src="https://i.imgur.com/9t3fDgT.png" title=Logo" width="500"/></a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Version-1.0.5-blueviolet" alt="Project Version">
    <img src="https://img.shields.io/badge/License-MIT-success" alt="License">
</p>

## О библиотеке 💙
Библиотека **CrystalPayIO** предоставит удобное использование и интеграцию _[CrystalPay](https://crystalpay.io/) API_ в ваши проекты.

> [!TIP]
> **Документация CrystalPAY:** https://docs.crystalpay.io/

В данном репозитории вы найдете способы установки и использования библиотеки.
Если вы обнаружите баги или какие-либо проблемы при использовании прошу отписать в [телеграм](https://t.me/fsoky_community). Данный модуль будет поддерживаться и обновляться. Спасибо, хорошего настроения!
> [!NOTE]
> Чтобы получить _AUTH_LOGIN_ & _AUTH_SECRET_ перейдите в [телеграм бота](https://t.me/CrystalPAY_bot) и создайте новую кассу. \
> В настройках можете включить тестовые платежи.

## Установка 🧡
- Установка, используя пакетный менеджер pip
```
$ pip install crystalpayio
```
- Установка с GitHub *(требуется [git](https://git-scm.com/downloads))*
```
$ git clone https://github.com/Fsoky/crystalpayio
$ cd crystalpayio
$ python setup.py install
```
- Или
```
$ pip install git+https://github.com/Fsoky/crystalpayio
```

## Примеры использования 💜
- Шаблон
```py
import asyncio
from crystalpayio import CrystalPayIO


async def main() -> None:
    async with CrystalPayIO("AUTH_LOGIN", "AUTH_SECRET") as crystal:
        ...


if __name__ == "__main__":
  asyncio.run(main())
```
- Доступные методы \
    `checkout` - Касса \
    `payment` - Платежи \
    `invoice` - Инвойсы (чеки) \
    `payoff` - Вывод средств \
    `ticker` - Доступные валюты и курс \
    `history` - История платежей/выводов/общая
```py
async with CrystalPayIO("AUTH_LOGIN", "AUTH_SECRET") as crystal:
    # Каждый метод хранится в свойстве, например касса:
    checkout = await crystal.checkout.me()
```

## Пример интеграции в телеграм-бота (aiogram 3.x) ❤
```py
import asyncio

from aiogram import Router, Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

from crystalpayio import CrystalPayIO

router = Router()
crystal = CrystalPayIO("AUTH_LOGIN", "AUTH_SECRET")


async def create_invoice() -> tuple:
    invoice = await crystal.invoice.create(
        100, # Цена
        5, # Время жизни чека (в минутах)
        amount_currency="RUB" # Валюта
    )
    return (invoice.url, invoice.id)


async def invoice_handler(id: str, message: Message) -> None:
    while True:
        invoice = await crystal.invoice.get(id)
        
        if invoice.state != "notpayed":
            await message.answer("Счёт успешно оплачен!")
        await asyncio.sleep(15) # Задержка


@router.message(CommandStart())
async def show_goods(message: Message) -> None:
    await message.answer(
        "🎃 Тыква - 100 РУБ.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="КУПИТЬ", callback_data="buy")]
            ]
        )
    )


@router.callback_query(F.data == "buy")
async def buy_handler(query: CallbackQuery) -> None:
    invoice_task = asyncio.create_task(create_invoice())
    invoice_result = await invoice_task

    await query.message.answer(f"Перейди по ссылке и оплати: {invoice_result[0]}")
    await query.answer()

    asyncio.create_task(invoice_handler(invoice_result[1], query.message))


async def main() -> None:
    bot = Bot("TOKEN")
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```

## Пример использования Webhook'ов 🕸
```py
import asyncio

from crystalpayio import CrystalPayIO, WebhookManager, PaymentEvent

from fastapi import FastAPI # pip install fastapi[all]
import uvicorn # pip install uvicorn

WEBHOOK_URL = "https://xxx-xxx-xxx.ngrok-free.app" # ngrok url
WEBHOOK_ENDPOINT = "/my-endpoint"

app = FastAPI()
crystal = CrystalPayIO("AUTH_LOGIN", "AUTH_SECRET")
wm = WebhookManager(app)

wm.register_webhook_endpoint(WEBHOOK_ENDPOINT) # Регистрируем путь к вебхуку


@wm.successfull_payment()
async def handle_successfull_event(event: PaymentEvent) -> None:
    print(event)


async def create_invoice() -> None:
    order = await crystal.invoice.create(
        10, # Сумма (в рублях)
        5, # Время жизни чека (в минутах)
        callback_url=f"{WEBHOOK_URL}{WEBHOOK_ENDPOINT}"
    )
    print(order.url)


if __name__ == "__main__":
    asyncio.run(create_invoice()) # Запуск функции
    uvicorn.run("test:app")
```