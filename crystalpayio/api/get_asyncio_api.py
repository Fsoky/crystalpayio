from typing import Literal

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
        """Cash register information."""
    
        response = await self._make_request("me/info", "post", json=self._DEFAULT_PAYLOAD)
        return CheckoutMe(**response)
    
    async def balance(self, hide_empty: bool=False) -> CheckoutBalance:
        """Cash balance receipt.

        :param hide_empty: Hide empty accounts.
        """

        self._DEFAULT_PAYLOAD.update({"hide_empty": hide_empty})

        response = await self._make_request("balance/info", "post", json=self._DEFAULT_PAYLOAD)
        return CheckoutBalance(
            error=response["error"],
            errors=response["errors"],
            balances=CheckoutBalancesCoins.model_validate(response["balances"])
        )
    

class _Payment(_BaseCrystalPayIO):

    async def methods(self) -> PaymentMethods:
        """Obtaining information on payment methods."""

        response = await self._make_request("method/list", "post", json=self._DEFAULT_PAYLOAD)
        return PaymentMethods(
            error=response["error"],
            errors=response["errors"],
            method=PaymentMethod.model_validate(response["methods"])
        )
    
    async def edit(self, method: str, extra_commission_percent: int, enabled: bool) -> BaseCrystalPayModels:
        """Changing payment method settings.
        
        :param method: Payment method, for example: LZTMARKET, BITCOIN.
        :param extra_commission_percent: Additional cash desk commission for the payment method (in percent).
        :param enabled: Enable/disable payment method.
        """

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
        amount_currency: str | None=None,
        required_method: str | None=None,
        description: str | None=None,
        redirect_url: str | None=None,
        callback_url: str | None=None,
        extra: str | None=None,
        payer_details: str | None=None
    ) -> PaymentInvoice:
        """Initiating payment transaction.

        :param amount: The amount of the transaction.
        :param lifetime: The duration (in seconds) for which the payment link is valid.
        :param type: The type of the transaction, either "purchase" or "topup" (default is "purchase").
        :param amount_currency: The currency code for the transaction amount (e.g., "USD").
        :param required_method: The specific payment method required for the transaction.
        :param description: A description or note for the transaction.
        :param redirect_url: The URL to redirect to after the payment is completed.
        :param callback_url: The URL for receiving callback notifications after payment.
        :param extra: Additional information or parameters for the transaction.
        :param payer_details: Additional details about the payer.
        """


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
        """Retrieve payment invoice information.

        :param id: The identifier of the payment invoice.
        """

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
        amount_currency: str | None=None,
        callback_url: str | None=None,
        extra: str | None=None
    ) -> PayoffCreate:
        """Processing withdrawal request.

        :param signature: The signature for authentication and authorization.
        :param method: The withdrawal method, for example: "bank_transfer", "crypto_withdrawal", etc.
        :param amount: The amount to be withdrawn.
        :param wallet: The wallet or account where the withdrawal should be processed.
        :param subtract_form: The source from which the withdrawal amount should be subtracted, either "balance" or "amount".
        :param amount_currency: The currency code for the withdrawal amount (e.g., "USD").
        :param callback_url: The URL for receiving callback notifications after withdrawal.
        :param extra: Additional information or parameters for the withdrawal.
        """

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
        """Submit a payoff action.

        :param signature: The signature for authentication and authorization.
        :param id: The identifier associated with the payoff action.
        """

        self._DEFAULT_PAYLOAD.update({"signature": signature, "id": id})

        response = await self._make_request("payoff/submit", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffAction.model_validate(response)
    
    async def cancel(self, signature: str, id: str) -> PayoffAction:
        """Cancel a payoff action.

        :param signature: The signature for authentication and authorization.
        :param id: The identifier associated with the payoff action.
        """
        self._DEFAULT_PAYLOAD.update({"signature": signature, "id": id})

        response = await self._make_request("payoff/cancel", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffAction.model_validate(response)
    
    async def get(self, id: str) -> PayoffAction:
        """Retrieve payoff action information.

        :param id: The identifier of the payoff action.
        """

        self._DEFAULT_PAYLOAD.update({"id": id})

        response = await self._make_request("payoff/info", "post", json=self._DEFAULT_PAYLOAD)
        return PayoffAction.model_validate(response)
    

class _Ticker(_BaseCrystalPayIO):

    async def ticker_list(self) -> Tickers:
        """Retrieve a list of tickers."""

        response = await self._make_request("ticker/list", "post", json=self._DEFAULT_PAYLOAD)
        return Tickers.model_validate(response)

    async def get(self) -> TickersData:
        """Retrieve ticker data."""

        response = await self._make_request("ticker/get", "post", json=self._DEFAULT_PAYLOAD)
        return TickersData.model_validate(response)
    

class _History(_BaseCrystalPayIO):

    async def payments(self, page: int, items: int) -> HistoryPayments:
        """Retrieve payment history.

        :param page: The page number of the payment history.
        :param items: The number of items per page in the payment history.
        """

        self._DEFAULT_PAYLOAD.update({"page": page, "items": items})

        response = await self._make_request("history/payments", "post", json=self._DEFAULT_PAYLOAD)
        return HistoryPayments.model_validate(response)
    
    async def payoffs(self, page: int, items: int) -> HistoryPayoffs:
        """Retrieve payoff history.

        :param page: The page number of the payoff history.
        :param items: The number of items per page in the payoff history.
        """

        self._DEFAULT_PAYLOAD.update({"page": page, "items": items})

        response = await self._make_request("history/payments", "post", json=self._DEFAULT_PAYLOAD)
        return HistoryPayoffs.model_validate(response)
    
    async def summary(self) -> HistorySummary:
        """Retrieve summary of payment and payoff history."""

        response = await self._make_request("history/summary", "post", json=self._DEFAULT_PAYLOAD)
        return HistorySummary.model_validate(response)