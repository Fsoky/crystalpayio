# AIOCrystalPay - Nice and easy

> **_Модуль в разработке, сейчас недоступны методы callback_**

## Установка 💾
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

## Примеры использования:
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
