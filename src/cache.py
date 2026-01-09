import json

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from random import choice
from typing import Any, Protocol


class EvictionPolicyType(Enum):
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    MRU = "mru"
    RANDOM = "random"

class KeyType(Enum):
    READABLE = "readable"
    HASHED = "hashed"



@dataclass
class CacheConfig:
    name: str
    eviction_policy: EvictionPolicyType
    key_type: KeyType
    max_age_seconds: int = 0
    max_count: int = 0
    max_size_bytes: int = 0


@dataclass
class CacheMetadata:
    created_utc_timestamp: float
    last_accessed_utc_timestamp: float
    times_accessed: int
    hits: int




@dataclass
class CachedCall:
    value: Any
    utc_timestamp: float
    access_count: int


def get_utc_timestamp() -> float:
    return datetime.now(timezone.utc).timestamp()


class EvictionPolicy(Protocol):
    def get_next_key_to_delete(self, cache: dict[str, CachedCall]) -> str:
        ...

def _get_least_recently_used_key(cache: dict[str, CachedCall]) -> str:
    for key, cache_entry in cache.items():



class ColdHardCache:
    def __init__(self):
        self.cache: dict[str, CachedCall] = {}
        self.eviction_policy: EvictionPolicy = None
        self.config: CacheConfig = None

    def store():
        pass

    def retrieve(self, key: str):
        cache_entry = self.cache[key]
        cache_entry.access_count += 1
        cache_entry.utc_timestamp = get_utc_timestamp()
        return cache_entry.value

    def purge_expired(self):
        for key in self.cache:
            if not self._entry_is_current(key):
                self.cache.pop(key)
                # TODO: add log

    def _entry_is_current(self, key) -> bool:
        """
        Given a key, returns True if that key's cache entry is olde
        """
        max_age = self.config.max_age_seconds
        if max_age <= 0:
            return True
        current_time = get_utc_timestamp()
        entry_timestamp = self.cache[key].utc_timestamp
        entry_age = current_time - entry_timestamp
        return entry_age > max_age

    def clear(self):
        self.cache = {}

    def reset():
        pass

    def read_cache_file():
        pass

    def write_cache_file():
        pass

    @property
    def least_recently_used_key():
        pass

    @property
    def least_frequently_used_key():
        pass

    @property
    def oldest_key():
        pass

    def __contains__(self, key: str) -> bool:
        return key in self.cache

    def __len__(self) -> int:
        return len(self.cache)

    def __repr__(self) -> str:
        pass

    def __enter__(self) -> None:
        pass

    def __exit__(self, *args, **kwargs):
        pass
