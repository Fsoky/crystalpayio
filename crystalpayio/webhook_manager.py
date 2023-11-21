from typing import Callable

from fastapi import FastAPI, Request

from .crystalpayio import CrystalPayIO
from .utils.models import PaymentEvent


class WebhookManager:

    def __init__(self, app: FastAPI) -> None:
        """Initialize the WebhookManager.

        :param app: The FastAPI application instance.
        """

        self._app = app
        self._successfull_callbacks = []
    
    def successfull_payment(self) -> Callable:
        """
        Decorator to register a callback function for handling successful events.
        """

        def decorator(func: Callable) -> Callable:
            self._successfull_callbacks.append(func)
            return func

        return decorator
        
    async def _handle_webhook(self, request: Request) -> None:
        data = await request.json()
        event = PaymentEvent.model_validate(data)

        if event.state == "payed":
            [
                await callback(event)
                for callback in self._successfull_callbacks
            ]
            return {"message": "Successfull payment!"}

    def register_webhook_endpoint(self, endpoint: str="/payment-webhook") -> None:
        """Endpoint registration webhook for event processing
        
        :param endpoint: Endpoint name
        """

        self._app.post(endpoint)(self._handle_webhook)