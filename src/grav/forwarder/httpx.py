import logging
from urllib.parse import urlparse, ParseResult

import httpx

from .base import BaseForwarder, Request, Response

logger = logging.getLogger(__name__)


class HttpxForwarder(BaseForwarder):
    def __init__(self, new_origin: ParseResult) -> None:
        super().__init__()
        self._NEW_ORIGIN = new_origin
        self._CLIENT = httpx.AsyncClient()

    async def forward(self, request: Request) -> Response:
        logger.info(f"forwarding request to {self._NEW_ORIGIN.geturl()}")
        old_url = urlparse(str(request.url))
        new_url = old_url._replace(
            scheme=self._NEW_ORIGIN.scheme, netloc=self._NEW_ORIGIN.netloc
        )
        logger.debug(f"new url is {new_url.geturl()}")

        fwd_request = self._CLIENT.build_request(
            request.method,
            new_url.geturl(),
            headers=request.headers,
            params=request.query_params,
            content=await request.body(),
        )

        response = await self._CLIENT.send(fwd_request)
        logger.debug("request forwarded, returning response")

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response.headers,
        )
