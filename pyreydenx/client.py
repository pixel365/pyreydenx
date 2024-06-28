import os
from typing import Optional, Dict

import httpx

from .exceptions import (
    InvalidCredentialsError,
    UnauthorizedError,
    NotFoundError,
    TooManyRequestsError,
    UnknownError,
)
from .model.token import Token

BASE_URL = "https://api.reyden-x.com/v1"


class Client:
    __slots__ = (
        "username",
        "password",
        "timeout",
        "token",
    )

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ):
        email = email or os.getenv("REYDENX_EMAIL")
        password = password or os.getenv("REYDENX_PASSWORD")

        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        self.username = email
        self.password = password
        self.timeout = timeout or httpx.Timeout(10.0)
        self.token = None
        self.auth()

    @property
    def is_authenticated(self) -> bool:
        return self.token is not None and self.token.is_valid

    def auth(self):
        r = httpx.post(
            f"{BASE_URL}/token/",
            data={
                "username": self.username,
                "password": self.password,
            },
            headers={
                "Accept": "application/json",
            },
            timeout=5,
        )
        if r.status_code == httpx.codes.OK:
            self.token = Token(**r.json())
        else:
            self.token = None
            raise InvalidCredentialsError

    def request(
        self, method: str, path: str, payload: Optional[Dict] = None
    ) -> Optional[Dict]:
        if not self.is_authenticated:
            raise UnauthorizedError

        headers = {
            "Authorization": f"Bearer {self.token.access_token}",
            "Accept": "application/json",
        }
        path = f"{BASE_URL}{path}"
        match method:
            case "POST":
                r = httpx.post(
                    path, json=payload, headers=headers, timeout=self.timeout
                )
            case "PATCH":
                r = httpx.patch(path, headers=headers, timeout=self.timeout)
            case _:
                r = httpx.get(path, headers=headers, timeout=self.timeout)

        match r.status_code:
            case httpx.codes.OK:
                return r.json()
            case httpx.codes.UNAUTHORIZED:
                raise UnauthorizedError
            case httpx.codes.NOT_FOUND:
                raise NotFoundError
            case httpx.codes.TOO_MANY_REQUESTS:
                raise TooManyRequestsError
            case _:
                raise UnknownError

    def get(self, path: str) -> Optional[Dict]:
        return self.request("GET", path)

    def post(self, path: str, payload: Dict) -> Optional[Dict]:
        return self.request("POST", path, payload)

    def patch(self, path: str) -> Optional[Dict]:
        return self.request("PATCH", path)
