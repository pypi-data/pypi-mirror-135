from typing import NamedTuple, Optional

from ruteni.utils.dns import RecordList


class Record(NamedTuple):
    host: str
    priority: int
    ttl: int
    type: str = "MX"


class DNSMock:
    def __init__(self, domains: dict[str, list[tuple[str, int, int]]]) -> None:
        self.domains = domains

    async def query_mx(self, domain: str) -> Optional[RecordList]:
        if domain not in self.domains:
            return None
        return [Record(*fields) for fields in self.domains[domain]]  # type: ignore
