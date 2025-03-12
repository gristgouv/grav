import enum
from abc import ABC, abstractmethod


class AVScanResult(enum.Enum):
    SAFE = enum.auto()
    MALWARE = enum.auto()
    FAIL = enum.auto()


class BaseAVScanner(ABC):
    @abstractmethod
    async def process(self, file) -> AVScanResult:
        pass
