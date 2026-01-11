import json

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from random import choice
from typing import Any, Protocol


TEMP_TEST_FILE_PATH = Path(__file__).parent / "TEMP_CACHE_TEST.json"
CACHE_KEY = "cache"

VALUE_INDEX = 0
STORED_TIMESTAMP_INDEX = 1
ACCESSED_TIMESTAMP_INDEX = 2
ACCESS_COUNT_INDEX = 3


# @dataclass
# class CacheConfig:
#     name: str
#     eviction_policy: EvictionPolicyType
#     key_type: KeyType
#     max_age_seconds: int = 0
#     max_count: int = 0
#     max_size_bytes: int = 0


# @dataclass
# class CacheMetadata:
#     created_utc_timestamp: float
#     last_accessed_utc_timestamp: float
#     times_accessed: int
#     hits: int

#     @classmethod
#     def new_metadata(cls):
#         now = get_utc_timestamp()
#         return CacheMetadata(
#             created_utc_timestamp = now,
#             last_accessed_utc_timestamp = now,
#             times_accessed = 0,
#             hits = 0,
#         )


def get_utc_timestamp() -> float:
    return datetime.now(timezone.utc).timestamp()


@dataclass
class CachedCall:
    value: Any
    stored_timestamp: float
    accessed_timestamp: float | None
    access_count: int

    def as_tuple(self) -> tuple:
        return (
            self.value,
            self.stored_timestamp,
            self.accessed_timestamp,
            self.access_count
        )
    
    @classmethod
    def new_from_tuple(cls, t: tuple):
        value, stored, accessed, count = t
        return CachedCall(
            value=value,
            stored_timestamp=stored,
            accessed_timestamp=accessed,
            access_count=count,
        )


class JsonCache:
    def __init__(
        self,
        cache_file_path: Path,
        cache: dict[str, CachedCall] | None = None
    ):
        self.cache_file_path = cache_file_path
        if cache is None:
            cache = {}
        self.cache = cache
    
    def _read_cache_file(self) -> None:
        with open(self.cache_file_path, "r") as cache_file:
            file_contents: dict[str, CachedCall] = json.load(cache_file)
        self.cache = file_contents

    def _write_cache_file(self) -> None:
        with open(self.cache_file_path, "w") as cache_file:
            json.dump(self.cache, cache_file)

    def store(self, key: str, value: Any) -> None:
        cache_entry = CachedCall(
            value=value,
            stored_timestamp=get_utc_timestamp(),
            accessed_timestamp=None,
            access_count=0,
        )
        self.cache[key] = cache_entry.as_tuple()
    
    def retrieve(self, key: str) -> Any:
        entry = CachedCall.new_from_tuple(self.cache[key])
        entry.access_count += 1
        entry.accessed_timestamp = get_utc_timestamp()
        return entry.value
    
    def _sorted_keys(self):
        pass
    
    @property
    def least_recently_used_key(self) -> str:
        lru_timestamp = None
        for key, cache_tuple in self.cache.items():
            pass

    @property
    def least_frequently_used_key(self) -> str:
        pass

    @property
    def random_key(self) -> str:
        return choice(self.cache.keys())

    @property
    def most_recently_used_key(self) -> str:
        pass

    @property
    def oldest_key(self) -> str:
        pass
    
    def __contains__(self, key: str) -> bool:
        return key in self.cache

    def __len__(self) -> int:
        return len(self.cache)