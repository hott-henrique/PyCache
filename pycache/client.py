""" PyCache Client Module. """

import os
import shutil
import typing as t

import pycache.exceptions as exc
import pycache.standard as std
from pycache.cache import Cache


class Client:
    """Represent a connection between python and the cache manager.

    :param name: Name of client to connect with.
    :type name: AnyStr
    """

    def __init__(self, name: t.AnyStr = 'PyCache') -> None:
        self.__name = name
        self.__client_path = os.path.abspath(name)

        os.makedirs(self.__client_path, exist_ok=True)

    def create_cache(self, cache: t.AnyStr, **kwargs) -> Cache:
        """Create an cache to save python objects.

        :param cache: The name to identify the cache.
        :type cache: AnyStr

        :param overwrite_existent: Flag to delete the old cache in case it exists, defaults to `False`.
        :type overwrite_existent: bool, optional

        :param ignore_existent: Flag to not raise exception when cache already exists, defaults to `False`.
        :type ignore_existent: bool, optional

        :raises ExistentCacheCreation: When trying to create an already existent cache and the colision method was not defined.
        """
        hcache = std.hash_identifier(cache)
        cache_path = os.path.join(self.__client_path, hcache)

        if os.path.isdir(cache_path):
            if kwargs.get('overwrite_existent', False):
                self.delete_cache(cache)
            elif kwargs.get('ignore_existent', False):
                return self.get_cache(cache)
            else:
                raise exc.ExistentCacheCreation(cache, self.__name)

        return Cache(cache, self.__name, create=True)

    def get_cache(self, cache: t.AnyStr) -> Cache:
        """Get an already created cache.

        :param cache: The cache.
        :type cache: AnyStr

        :raises InexistentCacheAccess: When trying to acces an inexistent cache.
        """
        hcache = std.hash_identifier(cache)

        cache_path = os.path.join(self.__client_path, hcache)

        if not os.path.isdir(cache_path):
            raise exc.InexistentCacheAccess(cache, self.__name)

        return Cache(cache, self.__name, create=False)

    def delete_cache(self, cache: t.AnyStr, **kwargs) -> None:
        """Delete an already created cache.

        :param cache: The cache to be deleted.
        :type cache: AnyStr

        :param ignore_inexistent: Flag to not raise exception when cache do not exists, defaults to `False`.
        :type ignore_inexistent: bool, optional

        :raises InexistentCacheAccess: When deleting an inexistent cache and `ignore_inexistent` is `False`.
        """
        hcache = std.hash_identifier(cache)

        cache_path = os.path.join(self.__client_path, hcache)

        if not os.path.isdir(cache_path):
            if kwargs.get('ignore_inexistent', False):
                return
            raise exc.InexistentCacheAccess(cache, self.__name)

        shutil.rmtree(cache_path)
