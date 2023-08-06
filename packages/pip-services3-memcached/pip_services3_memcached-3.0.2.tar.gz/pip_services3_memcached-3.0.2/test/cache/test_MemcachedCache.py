# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from pip_services3_memcached.cache.MemcachedCache import MemcachedCache
from test.fixtures.CacheFixture import CacheFixture


class TestMemcachedCache:
    _cache: MemcachedCache
    _fixture: CacheFixture

    def setup_method(self):
        host = os.environ.get('MEMCACHED_SERVICE_HOST') or 'localhost'
        port = os.environ.get('MEMCACHED_SERVICE_PORT') or 11211

        self._cache = MemcachedCache()

        config = ConfigParams.from_tuples(
            'connection.host', host,
            'connection.port', port
        )

        self._cache.configure(config)

        self._fixture = CacheFixture(self._cache)

        self._cache.open(None)

    def teardown_method(self):
        self._cache.close(None)

    def test_store_and_retrieve(self):
        self._fixture.test_store_and_retrieve()

    def test_retrieve_expired(self):
        self._fixture.test_retrieve_expired()

    def test_remove(self):
        self._fixture.test_remove()
