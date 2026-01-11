from pathlib import Path
from tempfile import NamedTemporaryFile
from random import randint

import pytest

from src.cache import JsonCache

@pytest.fixture
def random_key_value_pair():
    key = randint(0, 100)
    value = randint(0, 100)
    return str(key), str(value)

@pytest.fixture
def known_key_value_pair():
    key = "key"
    value = "value"
    return key, value


@pytest.fixture
def temp_cache_file():
    with NamedTemporaryFile() as temp_file:
        yield temp_file.name


@pytest.fixture
def basic_cache(temp_cache_file, known_key_value_pair):
    key, value = known_key_value_pair
    cache = JsonCache(temp_cache_file)
    cache.store(key, value)
    return cache


def test_json_cache_extant():
    test_cache = JsonCache
    assert test_cache is not None


def test_json_cache_basic_retrieval(random_key_value_pair):
    # Given
    fake_path = Path(__file__)
    cache = JsonCache(fake_path)
    cache_key, stored = random_key_value_pair
    
    # When
    cache.store(cache_key, stored)
    retrieved = cache.retrieve(cache_key)

    # Then
    assert stored == retrieved


def test_json_cache_file_storage(temp_cache_file, random_key_value_pair):
    # Given
    in_cache = JsonCache(temp_cache_file)
    out_cache = JsonCache(temp_cache_file)
    cache_key, stored = random_key_value_pair

    # When
    in_cache.store(cache_key, stored)
    in_cache._write_cache_file()
    out_cache._read_cache_file()
    retrieved = out_cache.retrieve(cache_key)

    # Then
    assert stored == retrieved


def test_json_cache_contains(basic_cache, known_key_value_pair):
    key, _ = known_key_value_pair
    assert key in basic_cache


def test_json_cache_len(basic_cache):
    assert len(basic_cache) == 1
    basic_cache.store("test", 0)
    assert len(basic_cache) == 2

def test_json_cache_clear(basic_cache, known_key_value_pair):
    # Given
    key, _ = known_key_value_pair
    assert key in basic_cache
    
    # When
    basic_cache.clear()
    
    # Then
    assert key not in basic_cache
