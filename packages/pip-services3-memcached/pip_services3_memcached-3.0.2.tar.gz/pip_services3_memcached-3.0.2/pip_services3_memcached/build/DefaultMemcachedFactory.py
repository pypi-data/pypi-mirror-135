# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from pip_services3_memcached.cache.MemcachedCache import MemcachedCache
from pip_services3_memcached.lock.MemcachedLock import MemcachedLock


class DefaultMemcachedFactory(Factory):
    """
    Creates Memcached components by their descriptors.

    See: :class:`MemcachedCache <pip_services3_memcached.cache.MemcachedCache.MemcachedCache>`,
    :class:`MemcachedLock <pip_services3_memcached.lock.MemcachedLock.MemcachedLock>`,
    """
    __MemcachedCacheDescriptor = Descriptor("pip-services", "cache", "memcached", "*", "1.0")
    __MemcachedLockDescriptor = Descriptor("pip-services", "lock", "memcached", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultMemcachedFactory.__MemcachedLockDescriptor, MemcachedLock)
        self.register_as_type(DefaultMemcachedFactory.__MemcachedCacheDescriptor, MemcachedCache)
