# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from pip_services3_memcached.lock.MemcachedLock import MemcachedLock
from test.fixtures.LockFixture import LockFixture


class TestMemcachedLock:
    _lock: MemcachedLock
    _fixture: LockFixture

    def setup_method(self):
        host = os.environ.get('MEMCACHED_SERVICE_HOST') or 'localhost'
        port = os.environ.get('MEMCACHED_SERVICE_PORT') or 11211

        self._lock = MemcachedLock()

        config = ConfigParams.from_tuples(
            'connection.host', host,
            'connection.port', port
        )

        self._lock.configure(config)

        self._fixture = LockFixture(self._lock)

        self._lock.open(None)

    def teardown_method(self):
        self._lock.close(None)

    def test_try_acquire_lock(self):
        self._fixture.test_try_acquire_lock()

    def test_acquire_lock(self):
        self._fixture.test_acquire_lock()

    def test_release_lock(self):
        self._fixture.test_release_lock()
