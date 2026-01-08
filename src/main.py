from pathlib import Path
from enum import Enum


class EvictionPolicy(Enum):
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    MRU = "mru"
    RANDOM = "random"

class KeyType(Enum):
    READABLE = "readable"
    HASHED = "hashed"


def cache():
    pass


def get_timestamp():
    pass


class ColdHardCache:
    def __init__(self):
        pass

