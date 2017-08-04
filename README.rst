=============================
django-atom
=============================

.. image:: https://badge.fury.io/py/django-atom.png
    :target: https://badge.fury.io/py/django-atom

.. image:: https://travis-ci.org/ad-m/django-atom.png?branch=master
    :target: https://travis-ci.org/ad-m/django-atom

A different stuff for Django to faster make a world a better place.

Documentation
-------------

The full documentation is at https://django-atom.readthedocs.org.

Quickstart
----------

Install django-atom::

    pip install django-atom

Then use it in a project::

    import atom

Extensions
----------

slugify
#######

Example usage in ``settings.py`` add

.. code:: python

 AUTOSLUG_SLUGIFY_FUNCTION = 'atom.ext.slugify.slugifier.ascii_slugify'
    
Required ```unicode-slugify```, ```django-autoslug```.
