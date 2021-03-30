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

The **pytest-easy-server** package is a
`Pytest <https://docs.pytest.org/en/stable/>`_ plugin that provides a
:func:`~pytest_easy_server.server_definition` fixture that resolves to the set
of servers the tests should run against.

The set of servers is defined in a *server definition file* and the secrets
to access the servers are defined in a *vault file* in the formats defined
by the
`easy-server package <https://easy-server.readthedocs.io/en/stable/>`_.

The files to use and the server or group nickname to select for the test
can be specified in pytest options added by the plugin:

.. code-block:: text

    --es-server-file=FILE   Use the specified server definition file.
                            Default: server.yml in current directory.

    --es-vault-file=FILE    Use the specified vault file.
                            Default: vault.yml in current directory.

    --es-nickname=NICKNAME  Use the server or server group with this
                            nickname to test against.
                            Default: default server or server group
                            specified in the server definition file.


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
.. _`Format of server definition file`: https://pytest-easy-server.readthedocs.io/en/latest/usage.html#format-of-server-definition-file
.. _`Protecting secrets`: https://pytest-easy-server.readthedocs.io/en/latest/usage.html#protecting-secrets
.. _`Derived Pytest fixtures`: https://pytest-easy-server.readthedocs.io/en/latest/usage.html#derived-pytest-fixtures
.. _`server_definition`: https://pytest-easy-server.readthedocs.io/en/latest/api.html#server-definition-fixture
.. _`ServerDefinition`: https://pytest-easy-server.readthedocs.io/en/latest/api.html#serverdefinition-class
.. _`Documentation`: https://pytest-easy-server.readthedocs.io/en/latest/
.. _`Change log`: https://pytest-easy-server.readthedocs.io/en/latest/changes.html
