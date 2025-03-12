from abc import ABC, abstractmethod

from starlette.requests import Request
from starlette.responses import Response


class BaseForwarder(ABC):
    @abstractmethod
    async def forward(self, request: Request) -> Response:
        pass
