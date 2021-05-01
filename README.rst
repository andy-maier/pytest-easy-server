pytest-easy-server - Pytest plugin for easy testing against servers
===================================================================

.. image:: https://badge.fury.io/py/pytest-easy-server.svg
    :target: https://pypi.python.org/pypi/pytest-easy-server/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/pytest-easy-server/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/pytest-easy-server/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/pytest-easy-server/badge/?version=latest
    :target: https://readthedocs.org/projects/pytest-easy-server/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/pytest-easy-server/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/pytest-easy-server?branch=master
    :alt: Test coverage (master)


.. _`Overview`:

Overview
--------

The **pytest-easy-server** package is a `Pytest`_ plugin that provides a
`Pytest fixture`_ fixture `es_server`_ that resolves
to the set of servers the tests should run against.

The set of servers is defined in a *server file* (aka "easy-server file") and
the secrets to access the servers are defined in a *vault file* that is
referenced by the server file, in the formats defined by the
`easy-server package`_.

The files to use and the server or group nickname to select for the test, as
well as a schema file for validating the user-defined structure of certain
properties in the server and vault files, can be specified in pytest options
added by the plugin:

.. code-block:: text

    --es-file=FILE
                            Path name of the easy-server file to be used.
                            Default: es_server.yml in current directory.

    --es-nickname=NICKNAME
                            Nickname of the server or server group to test against.
                            Default: The default from the server file.

    --es-schema-file=FILE
                            Path name of the schema file to be used for validating the structure of
                            user-defined properties in the easy-server server and vault files.
                            Default: No validation.

    --es-encrypted          Require that the vault file (if specified) is encrypted and error out otherwise.
                            Default: Tolerate unencrypted vault file.


.. _`Documentation and change log`:

Documentation and change log
----------------------------

* `Documentation`_
* `Change log`_


License
-------

The pytest-easy-server project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/pytest-easy-server/master/LICENSE>`_.


.. # Links to documentation:

.. _`Pytest`: https://docs.pytest.org/en/stable/
.. _`Pytest fixture`: https://docs.pytest.org/en/stable/fixture.html
.. _`easy-server package`: https://easy-server.readthedocs.io/en/stable/
.. _`es_server`: https://pytest-easy-server.readthedocs.io/en/stable/api.html#es-server-fixture
.. _`Documentation`: https://pytest-easy-server.readthedocs.io/en/stable/
.. _`Change log`: https://pytest-easy-server.readthedocs.io/en/stable/changes.html
