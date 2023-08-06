=============================
django-exo-role
=============================

.. image:: https://badge.fury.io/py/django-exo-role.svg
    :target: https://badge.fury.io/py/django-exo-role

.. image:: https://travis-ci.org/exolever/django-exo-role.svg?branch=master
    :target: https://travis-ci.org/exolever/django-exo-role

.. image:: https://codecov.io/gh/exolever/django-exo-role/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-exo-role
  
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/django-exo-role/issues
    
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT


Use roles system with Django

Quickstart
----------

Install django-exo-role::

    pip install django-exo-role

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'exo_role',
        ...
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
