import json

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from random import choice
from typing import Any, Callable


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

class EvictionPolicy(Enum):
    LRU = 0
    LFU = 1
    RANDOM = 2
    MRU = 3
    FIFO = 4

class JsonCache:
    def __init__(
        self,
        cache_file_path: Path,
        cache: dict[str, CachedCall] | None = None,
        max_size: int = 10,
        max_age_seconds: timedelta | None = None,
        eviction_policy: EvictionPolicy = EvictionPolicy.LFU
    ):
        self.cache_file_path = cache_file_path
        if cache is None:
            cache = {}
        self.cache = cache
        self.max_size = max_size
        self.max_age_seconds = max_age_seconds
        self.eviction_policy = eviction_policy

    
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
    
    def clear(self) -> None:
        self.cache = {}
    
    def _sorted_keys(self, odering_index: int):
        return sorted(self.cache.items(), key=lambda x: x[-1][odering_index])
    
    @property
    def least_recently_used_key(self) -> str:
        sorted_keys = self._sorted_keys(ACCESSED_TIMESTAMP_INDEX)
        return sorted_keys[0][0]

    @property
    def least_frequently_used_key(self) -> str:
        sorted_keys = self._sorted_keys(ACCESS_COUNT_INDEX)
        return sorted_keys[0][0]

    @property
    def random_key(self) -> str:
        return choice(self.cache.keys())

    @property
    def most_recently_used_key(self) -> str:
        sorted_keys = self._sorted_keys(ACCESSED_TIMESTAMP_INDEX)
        return sorted_keys[0][-1]

    @property
    def oldest_key(self) -> str:
        sorted_keys = self._sorted_keys(STORED_TIMESTAMP_INDEX)
        return sorted_keys[0][0]
    
    def delete_key(self, key: str) -> None:
        self.cache.pop(key)
    
    def get_next_key_to_evict(self) -> str:
        eviction_policy_map = {
            EvictionPolicy.LRU: self.least_recently_used_key,
            EvictionPolicy.LFU: self.least_frequently_used_key,
            EvictionPolicy.MRU: self.most_recently_used_key,
            EvictionPolicy.RANDOM: self.random_key,
            EvictionPolicy.FIFO: self.oldest_key,
        }
        return eviction_policy_map.get(self.eviction_policy)()
        
    def cull_to_size(self):
        if self.max_size <= 0:
            return
        while len(self) > self.max_size:
            next_key = self.get_next_key_to_evict()
            self.delete_key(next_key)
    
    def clear_old_keys(self):
        if self.max_age_seconds <= 0:
            return
        now = get_utc_timestamp()
        for key, entry in reversed(self._sorted_keys(STORED_TIMESTAMP_INDEX)):
            if now - entry[STORED_TIMESTAMP_INDEX] > self.max_age_seconds:
                self.delete_key(key)
    
    def __contains__(self, key: str) -> bool:
        return key in self.cache

    def __len__(self) -> int:
        return len(self.cache)
    
    def __enter__(self) -> "JsonCache":
        self._read_cache_file()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.clear_old_keys()
        self.cull_to_size()
        self._write_cache_file()


def cache(
    func: Callable,
    max_age_seconds: int = 0,
    max_size: int = 0,
):
    def cache_wrapper(*args, **kwargs):
        cache_folder = Path(__file__).parent
        cache_file_name = f"{func.__name__}_cache.json"
        cache_file_path = cache_folder / cache_file_name
        call_str = f"{args}|{kwargs}"
        with JsonCache(cache_file_path) as j_cache:
            if call_str not in j_cache:
                j_cache.store(call_str, func(*args, **kwargs))
            return j_cache.retrieve(call_str)
    return cache_wrapper