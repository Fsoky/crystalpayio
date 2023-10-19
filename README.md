# AIOCrystalPay - Nice and easy

> **_Модуль в разработке, сейчас недоступны методы callback_**

## Установка 💾
- Установка, используя пакетный менеджер pip
```
$ pip install aiocrystalpay
```
- Установка с GitHub *(требуется [git](https://git-scm.com/downloads))*
```
$ git clone https://github.com/Fsoky/aiocrystalpay
$ cd aiocrystalpay
$ python setup.py install
```
- Или
```
$ pip install git+https://github.com/Fsoky/aiocrystalpay
```

## Примеры использования:
- Шаблон
```py
import asyncio
from aiocrystalpay import AIOCrystalPay


async def main() -> None:
    async with AIOCrystalPay("AUTH_LOGIN", "AUTH_SECRET") as crystal:
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
async with AIOCrystalPay("AUTH_LOGIN", "AUTH_SECRET") as crystal:
    # Каждый метод хранится в свойстве, например касса:
    checkout = await crystal.checkout.me()
```
