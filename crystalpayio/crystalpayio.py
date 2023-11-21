from crystalpayio.utils.base import _BaseCrystalPayIO
from crystalpayio.api.get_asyncio_api import (
    _Checkout,
    _Payment,
    _Invoice,
    _Payoff,
    _Ticker,
    _History
)

__all__ = ["CrystalPayIO"]


class CrystalPayIO(_BaseCrystalPayIO):
    
    @property
    def checkout(self) -> _Checkout:
        return _Checkout(self._login, self._secret)
    
    @property
    def payment(self) -> _Payment:
        return _Payment(self._login, self._secret)
    
    @property
    def invoice(self) -> _Invoice:
        return _Invoice(self._login, self._secret)
    
    @property
    def payoff(self) -> _Payoff:
        return _Payoff(self._login, self._secret)
    
    @property
    def ticker(self) -> _Ticker:
        return _Ticker(self._login, self._secret)
    
    @property
    def history(self) -> _History:
        return _History(self._login, self._secret)