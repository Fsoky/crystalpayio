from typing import Literal, Optional

from ..utils.base import _BaseCrystalPayIO
from ..utils.models import (
    BaseCrystalPayModels,
    CheckoutMe,
    CheckoutBalance,
    CheckoutBalancesCoins,
    PaymentMethods,
    PaymentMethod,
    PaymentInvoice,
    PaymentInvoiceInfo,
    PayoffCreate,
    PayoffAction,
    Tickers,
    TickersData,
    HistoryPayments,
    HistoryPayoffs,
    HistorySummary
)


class _Checkout(_BaseCrystalPayIO):

    async def me(self) -> CheckoutMe:
        response = await self._make_request("me/info", "post", json=self._DEFAULT_PAYLOAD)
        return CheckoutMe(**response)
    
    async def balance(self, hide_empty: bool=False) -> CheckoutBalance:
        self._DEFAULT_PAYLOAD.update({"hide_empty": hide_empty})

        response = await self._make_request("balance/info", "post", json=self._DEFAULT_PAYLOAD)
        return CheckoutBalance(
            error=response["error"],
            errors=response["errors"],
            balances=CheckoutBalancesCoins.model_validate(response["balances"])
        )
    

class _Payment(_BaseCrystalPayIO):

    async def methods(self) -> PaymentMethods:
        response = await self._make_request("method/list", "post", json=self._DEFAULT_PAYLOAD)
        return PaymentMethods(
            error=response["error"],
            errors=response["errors"],
            method=PaymentMethod.model_validate(response["methods"])
        )
    
    async def edit(self, method: str, extra_commission_percent: int, enabled: bool) -> BaseCrystalPayModels:
        self._DEFAULT_PAYLOAD.update(
            {
                "method": method,
                "extra_commission_percent": extra_commission_percent,
                "enabled": enabled,
            }
        )

        response = await self._make_request("method/edit", "post", json=self._DEFAULT_PAYLOAD)
        return BaseCrystalPayModels.model_validate(response)


class _Invoice(_BaseCrystalPayIO):

    async def create(
        self,
        amount: float | int,
        lifetime: int,
        type: Literal["purchase", "topup"]="purchase",
        *,
        amount_currency: Optional[str] | None=None,
        required_method: Optional[str] | None=None,
        description: Optional[str] | None=None,
        redirect_url: Optional[str] | None=None,
        callback_url: Optional[str] | None=None,
        extra: Optional[str] | None=None,
        payer_details: Optional[str] | None=None
    ) -> PaymentInvoice:
        self._DEFAULT_PAYLOAD.update(
            {
                "amount": amount,
                "lifetime": lifetime,
                "type": type,
                "amount_currency": amount_currency,
                "required_method": required_method,
                "description": description,
                "redirect_url": redirect_url,
                "callback_url": callback_url,
                "extra": extra,
                "payer_details": payer_details   
            }
        )

        response = await self._make_request("invoice/create", "post", json=self._DEFAULT_PAYLOAD)
        return PaymentInvoice.model_validate(response)
    
    async def get(self, id: str) -> PaymentInvoiceInfo:
        self._DEFAULT_PAYLOAD.update({"id": id})

        response = await self._make_request("invoice/info", "post", json=self._DEFAULT_PAYLOAD)
        return PaymentInvoiceInfo.model_validate(response)


class _Payoff(_BaseCrystalPayIO):

    async def create(
        self,
        signature: str,
        method: str,
        amount: int | float,
        wallet: str,
        subtract_form: Literal["balance", "amount"],
        *,
        amount_currency: Optional[str] | None=None,
        callback_url: Optional[str] | None=None,
        extra: Optional[str] | None=None
    ) -> PayoffCreate:
        self._DEFAULT_PAYLOAD.update(
            {
                "signature": signature,
                "method": method,
                "amount": amount,
                "wallet": wallet,
                "subtract_form": subtract_form,
                "amount_currency": amount_currency,
                "callback_url": callback_url,
                "extra": extra
            }
        )

        response = await self._make_request("payoff/create", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffCreate.model_validate(response)
    
    async def submit(self, signature: str, id: str) -> PayoffAction:
        self._DEFAULT_PAYLOAD.update({"signature": signature, "id": id})

        response = await self._make_request("payoff/submit", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffAction.model_validate(response)
    
    async def cancel(self, signature: str, id: str) -> PayoffAction:
        self._DEFAULT_PAYLOAD.update({"signature": signature, "id": id})

        response = await self._make_request("payoff/cancel", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffAction.model_validate(response)
    
    async def get(self, id: str) -> PayoffAction:
        self._DEFAULT_PAYLOAD.update({"id": id})

        response = await self._make_request("payoff/info", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffAction.model_validate(response)
    

class _Ticker(_BaseCrystalPayIO):

    async def ticker_list(self) -> Tickers:
        response = await self._make_request("ticker/list", "post", json=self._DEFAULT_PAYLOAD)
        return Tickers.model_validate(response)

    async def get(self) -> TickersData:
        response = await self._make_request("ticker/get", "post", json=self._DEFAULT_PAYLOAD)
        return TickersData.model_validate(response)
    

class _History(_BaseCrystalPayIO):

    async def payments(self, page: int, items: int) -> HistoryPayments:
        self._DEFAULT_PAYLOAD.update({"page": page, "items": items})

        response = await self._make_request("history/payments", "post", json=self._DEFAULT_PAYLOAD)
        return HistoryPayments.model_validate(response)
    
    async def payoffs(self, page: int, items: int) -> HistoryPayoffs:
        self._DEFAULT_PAYLOAD.update({"page": page, "items": items})

        response = await self._make_request("history/payments", "post", json=self._DEFAULT_PAYLOAD)
        return HistoryPayoffs.model_validate(response)
    
    async def summary(self) -> HistorySummary:
        response = await self._make_request("history/summary", "post", json=self._DEFAULT_PAYLOAD)
        return HistorySummary.model_validate(response)