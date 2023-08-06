# -*- coding: utf-8 -*-
import datetime
import json
import time

from pip_services3_components.cache import ICache

KEY1: str = "key1"
KEY2: str = "key2"
KEY3: str = "key3"
KEY4: str = "key4"
KEY5: str = "key5"
KEY6: str = "key6"

VALUE1: str = "value1"
VALUE2: dict = {'val': "value2"}
VALUE3 = datetime.datetime.now()
VALUE4 = [1, 2, 3, 4]
VALUE5 = 12345
VALUE6 = None


class CacheFixture:

    def __init__(self, cache: ICache):
        self.__cache = cache

    def test_store_and_retrieve(self):
        self.__cache.store(None, KEY1, VALUE1, 5000)
        self.__cache.store(None, KEY2, VALUE2, 5000)
        self.__cache.store(None, KEY3, VALUE3, 5000)
        self.__cache.store(None, KEY4, VALUE4, 5000)
        self.__cache.store(None, KEY5, VALUE5, 5000)
        self.__cache.store(None, KEY6, VALUE6, 5000)

        time.sleep(0.5)

        val = self.__cache.retrieve(None, KEY1)
        assert val is not None
        assert VALUE1 == val

        val = self.__cache.retrieve(None, KEY2)
        assert val is not None
        assert VALUE2['val'] == val['val']

        val = self.__cache.retrieve(None, KEY3)
        assert val is not None
        assert json.loads(json.dumps(VALUE3, default=str)) == val

        val = self.__cache.retrieve(None, KEY4)
        assert val is not None
        assert len(val) == 4
        assert VALUE4[0] == val[0]

        val = self.__cache.retrieve(None, KEY5)
        assert val is not None
        assert VALUE5 == val

        val = self.__cache.retrieve(None, KEY6)
        assert val is None

    def test_retrieve_expired(self):
        self.__cache.store(None, KEY1, VALUE1, 1000)

        time.sleep(1.5)

        val = self.__cache.retrieve(None, KEY1)

        assert val is None

    def test_remove(self):
        self.__cache.store(None, KEY1, VALUE1, 1000)

        self.__cache.remove(None, KEY1)

        val = self.__cache.retrieve(None, KEY1)

        assert val is None
