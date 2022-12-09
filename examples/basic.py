import pycache as pyc

c = pyc.Client('__PyCache')

cache = c.create_cache('Tst', ignore_existent=True)

try:
    cache.save_obj('Receba', 1)
except pyc.ExistentObjectCreation:
    print(cache.load_obj('Receba'))
