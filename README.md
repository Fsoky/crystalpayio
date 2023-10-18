# AIOCrystalPay - Asynchronous wrapper for Crystal Pay API

> **_Модуль в разработке, сейчас недоступны методы withdraw_**

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
- Работа с кассой (Все методы доступны из свойства checkout)
```py
async with AIOCrystalPay("AUTH_LOGIN", "AUTH_SECRET") as crystal:
    checkout = await crystal.checkout.me() # Получение информации о кассе
```
