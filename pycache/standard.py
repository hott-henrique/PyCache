import hashlib
import typing as t


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
