""" PyCache Client Module. """

import hashlib
import os
import pickle
import shutil
import typing as t

import pycache.exceptions as exc


def hash_identifier(string: t.AnyStr) -> str:
    """ Hash function to generate valid file/directory names.

    :param string: String to execute hash
    :type string: AnyStr
    :return: Hash result.
    :rtype: str
    """
    return str(hashlib.md5(
        string.encode('utf-8'),
        usedforsecurity=False
    ).hexdigest())

class Client():
    """Represent a connection between python and the cache manager.

    :param name: Name of client to connect with.
    :type name: AnyStr
    """

    def __init__(self, name: t.AnyStr = 'PyCache') -> None:
        self.__name = name
        self.__client_path = os.path.abspath(name)

        os.makedirs(self.__client_path, exist_ok=True)

    def create_cache(self, cache: t.AnyStr, **kwargs) -> None:
        """Create an cache to save python objects.

        :param cache: The name to identify the cache.
        :type cache: AnyStr

        :param overwrite_existent: Flag to delete the old cache in case it exists, defaults to `False`.
        :type overwrite_existent: bool, optional

        :param ignore_existent: Flag to not raise exception when cache already exists, defaults to `False`.
        :type ignore_existent: bool, optional

        :raises ExistentCacheCreation: When trying to create an already existent cache and the colision method was not defined.
        """
        hcache = hash_identifier(cache)

        cache_path = os.path.join(self.__client_path, hcache)

        if os.path.isdir(cache_path):
            if kwargs.get('overwrite_existent', False):
                self.delete_cache(cache)
            elif kwargs.get('ignore_existent', False):
                return
            else:
                raise exc.ExistentCacheCreation(cache, self.__name)

        os.makedirs(cache_path)

    def delete_cache(self, cache: t.AnyStr, **kwargs) -> None:
        """Delete an already created cache.

        :param cache: The cache to be deleted.
        :type cache: AnyStr

        :param ignore_inexistent: Flag to not raise exception when cache do not exists, defaults to `False`.
        :type ignore_inexistent: bool, optional

        :raises InexistentCacheAccess: When deleting an inexistent cache and `ignore_inexistent` is `False`.
        """
        hcache = hash_identifier(cache)

        cache_path = os.path.join(self.__client_path, hcache)

        if not os.path.isdir(cache_path):
            if kwargs.get('ignore_inexistent', False):
                return
            raise exc.InexistentCacheAccess(cache, self.__name)

        shutil.rmtree(cache_path)

    def save_obj(self, cache: t.AnyStr, obj_identifier: t.AnyStr, obj: t.Any, **kwargs):
        """Save python object to the cache.

        :param cache: Cache handle to save `obj`.
        :type cache: AnyStr

        :param obj_identifier: String that will identify `obj`.
        :type obj_identifier: t.AnyStr

        :param obj: Object to save.
        :type obj: Any

        :param create_cache: Flag to create cache if it dont exists, defaults to `False`.
        :type create_cache: bool, optional

        :param overwrite_existent: Flag to overwrite an existent object, defaults to `False`.
        :type overwrite_existent: bool, optional

        :raises InexistentCacheAccess: If cache do not exists and `create_cache` is `False`.
        :raises ExistentObjectCreation: When trying to overwrite an object and `overwrite` is `False`.
        """
        hcache = hash_identifier(cache)

        if kwargs.get('create_cache', False):
            self.create_cache(cache, ignore_existent=True)

        cache_path = os.path.join(self.__client_path, hcache)

        if not os.path.exists(cache_path):
            raise exc.InexistentCacheAccess(cache, self.__name)

        hoid = hash_identifier(obj_identifier)

        obj_path = os.path.join(cache_path, hoid)

        if os.path.exists(obj_path) and not kwargs.get('overwrite_existent', False):
            raise exc.ExistentObjectCreation(obj_identifier, cache, self.__name)

        with open(obj_path, mode='wb') as file:
            pickle.dump(obj=obj, file=file)

    def load_obj(self, cache: t.AnyStr, obj_identifier: t.AnyStr, **kwargs) -> t.Any:
        """Load an object that was saved before.

        :param cache: Cache handle to load the object from.
        :type cache: AnyStr

        :param obj_identifier: String that identify the object to be loaded.
        :type obj_identifier: AnyStr

        :param exec: Callable to execute when obj_identifier was not found in cache, defaults to `None`.
        :type exec: Callable, optional

        :param pos_params: Positional parameters to pass to callable in `exec` argument, defaults to `list()`.
        :type pos_params: List[Any], optional

        :param key_params: Keyword parameters to pass to callable in `exec` argument, defaults to `dict()`.
        :type key_params: Dict[Any], optional

        :param save_ret: If `True` the object return will be saved in cache with identified as `obj_identifier` and returned. Otherwise, another atempt to load `obj_identifier` will be executed.
        :type save_ret: bool, optional

        :raises InexistentCacheAccess: When try to access an inexistent cache.
        :raises InexistentObjectAccess: When try to load an inexistent object and a method to generate the object was not provided.

        :return: The python object.
        :rtype: Any
        """
        hcache = hash_identifier(cache)

        cache_path = os.path.join(self.__client_path, hcache)

        if not os.path.exists(cache_path):
            raise exc.InexistentCacheAccess(cache, self.__name)

        hoid = hash_identifier(obj_identifier)

        obj_path = os.path.join(cache_path, hoid)

        if not os.path.exists(obj_path):
            func = kwargs.get('func', None)
            if func is not None:
                ret_object = func(*kwargs.get('pos_params', list()), **kwargs.get('key_params', dict()))
                if kwargs.get('save_ret', True):
                    self.save_obj(cache, obj_identifier, ret_object)
                    return ret_object
            raise exc.InexistentObjectAccess(obj_identifier, cache, self.__name)

        with open(obj_path, mode='rb') as file:
            return pickle.load(file=file)
