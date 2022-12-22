""" PyCache Cache Module. """

import os
import pickle
import typing as t

import pycache.exceptions as exc
import pycache.standard as std


class Cache:
    """Represent a connection between python and the cache manager.

    :param client: Name of client to connect with.
    :param cache: Name of cache to execute operations.
    :type cache: AnyStr
    """

    def __init__(self, cache: t.AnyStr, client: t.AnyStr = 'PyCache', **kwargs) -> None:
        cache_hash = std.hash_identifier(cache)

        self.__client = client
        self.__cache = cache

        self.__path = os.path.join(os.path.abspath(client), cache_hash)

        if kwargs.get('create', False):
            os.makedirs(self.__path)

    def save_obj(self, obj_identifier: t.AnyStr, obj: t.Any, **kwargs):
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

        :raises ExistentObjectCreation: When trying to overwrite an object and `overwrite` is `False`.
        """
        hoid = std.hash_identifier(obj_identifier)

        obj_path = os.path.join(self.__path, hoid)

        if os.path.exists(obj_path) and not kwargs.get('overwrite_existent', False):
            raise exc.ExistentObjectCreation(obj_identifier, self.__cache, self.__client)

        with open(obj_path, mode='wb') as file:
            pickle.dump(obj=obj, file=file)

    def load_obj(self, obj_identifier: t.AnyStr, **kwargs) -> t.Any:
        """Load an object that was saved before.

        :param cache: Cache handle to load the object from.
        :type cache: AnyStr

        :param obj_identifier: String that identify the object to be loaded.
        :type obj_identifier: AnyStr

        :raises InexistentObjectAccess: When try to load an inexistent object.

        :return: The python object.
        :rtype: Any
        """
        hoid = std.hash_identifier(obj_identifier)

        obj_path = os.path.join(self.__path, hoid)

        if not os.path.exists(obj_path):
            raise exc.InexistentObjectAccess(obj_identifier, self.__cache, self.__client)

        with open(obj_path, mode='rb') as file:
            return pickle.load(file=file)

    def delete_obj(self, obj_identifier: t.AnyStr) -> None:
        """Try to delete object in cache.

        :param obj_identifier: Identifier of object to be deleted.
        :type obj_identifier: AnyStr

        :raises InexistentObjectAccess: When try to delete inexistent object.
        """
        hoid = std.hash_identifier(obj_identifier)

        obj_path = os.path.join(self.__path, hoid)

        if not os.path.exists(obj_path):
            raise exc.InexistentObjectAccess(obj_identifier, self.__cache, self.__client)

        os.remove(obj_path)
