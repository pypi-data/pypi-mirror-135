# -*- coding: utf-8 -*-
from pip_services3_commons.errors import ConflictException
from pip_services3_components.lock.ILock import ILock

LOCK1: str = "lock_1"
LOCK2: str = "lock_2"
LOCK3: str = "lock_3"


class LockFixture:

    def __init__(self, lock: ILock):
        self.__lock = lock

    def test_try_acquire_lock(self):
        # Try to acquire lock for the first time
        ok = self.__lock.try_acquire_lock(None, LOCK1, 3000)
        assert ok is True

        # Try to acquire lock for the second time
        ok = self.__lock.try_acquire_lock(None, LOCK1, 3000)
        assert ok is False

        # Release the lock
        self.__lock.release_lock(None, LOCK1)

        # Try to acquire lock for the third time
        ok = self.__lock.try_acquire_lock(None, LOCK1, 3000)
        assert ok is True

        self.__lock.release_lock(None, LOCK1)

    def test_acquire_lock(self):
        # Acquire lock for the first time
        self.__lock.acquire_lock(None, LOCK2, 3000, 1000)

        # Acquire lock for the second time
        try:
            self.__lock.acquire_lock(None, LOCK2, 3000, 1000)
            assert False, 'Expected exception on the second lock attempt'
        except ConflictException:
            # Expected exception...
            pass

        # Release the lock
        self.__lock.release_lock(None, LOCK2)

        # Acquire lock for the third time
        self.__lock.acquire_lock(None, LOCK2, 3000, 1000)

        self.__lock.release_lock(None, LOCK2)

    def test_release_lock(self):
        # Acquire lock for the first time
        ok = self.__lock.try_acquire_lock(None, LOCK3, 3000)
        assert ok is True

        # Release the lock for the first time
        self.__lock.release_lock(None, LOCK3)

        # Release the lock for the second time
        self.__lock.release_lock(None, LOCK3)
