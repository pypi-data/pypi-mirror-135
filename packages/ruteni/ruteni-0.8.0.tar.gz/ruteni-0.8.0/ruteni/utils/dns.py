from typing import Optional, Protocol

import aiodns


class Record(Protocol):
    host: str
    priority: int
    ttl: int
    type: str = "MX"


# from pycares import ares_query_mx_result

RecordList = list[Record]  # ares_query_mx_result]


async def query_mx(domain: str, timeout: int = 3) -> Optional[RecordList]:
    resolver = aiodns.DNSResolver(timeout=timeout)
    try:
        return await resolver.query(domain, "MX")
    except aiodns.error.DNSError:
        return None
