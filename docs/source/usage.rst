Quick Start
===========

Installation
------------

To use PyCache, first clone it from GitHub:

SSH:

.. code-block:: console

   $ git clone git@github.com:hott-henrique/PyCache.git
   $ mv PyCache/pycache/ ..
   $ rm -rf PyCache

HTTPS:

.. code-block:: console

   $ git clone https://github.com/hott-henrique/PyCache.git
   $ mv PyCache/pycache/ ..
   $ rm -rf PyCache

GitHub CLI:

.. code-block:: console

   $ gh repo clone hott-henrique/PyCache
   $ mv PyCache/pycache/ ..
   $ rm -rf PyCache

Introduction
------------

Importing the library:

.. code-block:: python

    import pycache

Creating Clients
----------------

To create a Client use ``pycache.Client()`` class:

.. code-block:: python

    c = pycache.Client()

.. autofunction:: pycache.Client

Creating Caches
---------------

.. code-block:: python

    c.create_cache('C')

.. autofunction:: pycache.Client.create_cache

Saving and Loading Python Objects
---------------------------------

.. code-block:: python

    l = [ 1, 2, 3, 4, 5 ]
    c.save_obj('C', 'l', l)

.. autofunction:: pycache.Client.save_obj

.. code-block:: python

    print(c.load_obj('C', 'l'))
    >>> [1, 2, 3, 4, 5]

.. autofunction:: pycache.Client.load_obj
