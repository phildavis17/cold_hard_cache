import json

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Protocol



class EvictionPolicy(Enum):
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    MRU = "mru"
    RANDOM = "random"

class KeyType(Enum):
    READABLE = "readable"
    HASHED = "hashed"

@dataclass
class CachedCall:
    key: str
    value: Any
    utc_timestamp: float
    access_count: int


@dataclass
class CacheConfig:
    name: str
    eviction_policy: EvictionPolicy
    key_type: KeyType

@dataclass
class CacheMetadata:
    created_utc_timestamp: float
    last_accessed_utc_timestamp: float
    times_accessed: int
    hits: int

def get_utc_timestamp() -> float:
    return datetime.now(timezone.utc).timestamp()



class ColdHardCache:
    def __init__(self):
        pass

    def store():
        pass

    def retrieve():
        pass

    def purge_expired():
        pass

    def clear():
        pass

    def read_cache_file():
        pass

    def write_cache_file():
        pass

    def __contains__() -> bool:
        pass

    def __len__(self) -> int:
        pass

    def __repr__(self) -> str:
        pass

    def __enter__(self) -> None:
        pass

    def __exit__(self, *args, **kwargs):
        pass
