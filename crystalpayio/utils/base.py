import hashlib
from typing import Any, Literal

import aiohttp

from .exceptions import CrystalPayError


class _BaseCrystalPayIO:
    _BASE_API_URL: str = "https://api.crystalpay.io/v2"
    _DEFAULT_PAYLOAD = {"auth_login": "", "auth_secret": ""}

    def __init__(self, login: str, secret: str) -> None:
        self._login = login
        self._secret = secret

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        return None
    
    async def _make_request(self, endpoint: str, method: Literal["get", "post"]="get", **kwargs) -> Any:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            self._DEFAULT_PAYLOAD.update({"auth_login": self._login, "auth_secret": self._secret})

            response = await session.request(method, f"{self._BASE_API_URL}/{endpoint}/", **kwargs)
            data = await response.json()

            if data["error"]:
                raise CrystalPayError(*data["errors"])
            return data
    
    @classmethod
    def signature(cls, signature_string: str) -> str:
        """Generate a SHA-1 signature for a given string.

        :param signature_string: The string for which the signature needs to be generated.
        """

        return hashlib.sha1(str.encode(signature_string)).hexdigest()