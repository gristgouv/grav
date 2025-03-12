import enum
import hashlib
import logging
from urllib.parse import ParseResult

import anyio
import httpx

from .base import AVScanResult, BaseAVScanner

logger = logging.getLogger(__name__)


class SyndetectAVScanner(BaseAVScanner):
    def __init__(self, api_url: str, api_token: str, retries: int = 10) -> None:
        super().__init__()
        self._API_URL = api_url
        logger.debug(f"configured api url {self._API_URL}")
        self._API_TOKEN = api_token
        self._RETRIES = retries
        self._CLIENT = httpx.AsyncClient(
            base_url=self._API_URL,
            headers={"X-Auth-token": self._API_TOKEN},
        )

    class _IntermediateResult(enum.Enum):
        NOT_SCANNED = enum.auto()
        SCANNING = enum.auto()
        SAFE = enum.auto()
        MALWARE = enum.auto()

    async def process(self, file):
        digest = hashlib.file_digest(file, "sha256").hexdigest()
        logger.info(f"processing file with digest {digest}")
        scan_result = await self._check_sha256(digest)
        if scan_result == self._IntermediateResult.NOT_SCANNED:
            logger.debug(f"file {digest} is not scanned yet, submitting")
            await self._submit(file)
            logger.debug(f"file {digest} submitted")
            retries = 0
            while True:
                await anyio.sleep(5)
                logger.debug(f"file {digest} checking results (retry {retries})")
                scan_result = await self._check_sha256(digest)
                if scan_result != self._IntermediateResult.SCANNING:
                    break
                retries += 1
                if retries > self._RETRIES:
                    break
        logger.info(f"file {digest} is {scan_result}")
        if scan_result == self._IntermediateResult.MALWARE:
            return AVScanResult.MALWARE
        elif scan_result == self._IntermediateResult.SAFE:
            return AVScanResult.SAFE
        else:
            return AVScanResult.FAIL

    async def _submit(self, file):
        await self._CLIENT.post("/submit", files={"file": file})

    async def _check_sha256(self, sha256):
        logger.debug(f"checking result for file sha {sha256}")
        result = await self._CLIENT.get(f"/results/{sha256}")
        if result.status_code == 404:
            logger.debug(f"file sha {sha256} is not scanned yet")
            return self._IntermediateResult.NOT_SCANNED
        data = result.json()
        if data.get("done") == True and data.get("is_malware") == False:
            logger.debug(f"file sha {sha256} is safe")
            return self._IntermediateResult.SAFE
        elif data.get("done") == True and data.get("is_malware") == True:
            logger.debug(f"file sha {sha256} is malware")
            return self._IntermediateResult.MALWARE
        elif not data.get("done") == True:
            logger.debug(f"file sha {sha256} is still scanning")
            return self._IntermediateResult.SCANNING
