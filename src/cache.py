import json

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from random import choice
from typing import Any, Protocol





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

    @classmethod
    def new_metadata(cls):
        now = get_utc_timestamp()
        return CacheMetadata(
            created_utc_timestamp = now,
            last_accessed_utc_timestamp = now,
            times_accessed = 0,
            hits = 0,
        )


@dataclass
class CachedCall:
    value: Any
    utc_timestamp: float
    access_count: int


def get_utc_timestamp() -> float:
    return datetime.now(timezone.utc).timestamp()


class JsonCache:
    def __init__(
        self,
        cache_file_path: Path,
        cache: dict | None
    ):
        self.cache_file_path = cache_file_path
    
    def _read_cache_file(self) -> dict:
        with open(self.cache_file_path, "r") as cache_file:
            file_contents = json.load(cache_file)
        cache = file_contents.get("cache", {})
        return cache

    def _write_cache_file(self) -> None:
        with open(self.cache_file_path, "w") as cache_file:
            json.dump(self.cache, cache_file)
    

