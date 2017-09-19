.. _settings

Settings
=======
This package has all the static variables used by different modules. Mainly are static paths, database connection
parameters, emails, ...etc.

it consists of 3 files namely:

    - ``base.py``: Contains all the required settings used in production. The only required file to exist for production
    installation.
    - ``local.py``: Overrides some or all variables in ``base.py`` for local use. Mainly during development or local
    installation.
    - ``test.py``: Overrides some or all variables when running in testing environment. This is usually some temp
    path and connection parameters for testing database instances.

There is an extra file ``settings_no_password.py`` contains all the variables in ``base.py`` but with empty values.
It is only for saving the required variables in the public repository.

The ``__init__.py`` of this package is responsible for importing the proper variables simply by having the following
code

.. code-block:: python
    :emphasize-lines: 7,8,11,12

        from sys import argv

        try:
            from .base import *
        except:
            from settings_no_password import  *
        try:
            from .local import *
        except ImportError:
            pass
        if 'nosetests' in argv[0]:
            from .test import *

The whole required variables as in ``settings_no_password.py`` are as follows:

.. literalinclude:: ../../../settings/settings_no_password.py