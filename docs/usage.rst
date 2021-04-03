.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _`Usage`:

Usage
=====


.. _`Supported environments`:

Supported environments
----------------------

The **pytest-easy-server** package is supported in these environments:

* Operating Systems: Linux, macOS / OS-X, native Windows, Linux subsystem in
  Windows, UNIX-like environments in Windows.

* Python: 2.7, 3.4, and higher


.. _`Installation`:

Installation
------------

The following command installs the **pytest-easy-server** package and its
prerequisite packages into the active Python environment:

.. code-block:: bash

    $ pip install pytest-easy-server

When Pytest runs, it will automatically find the plugin and will show
its version, e.g.:

.. code-block:: text

    plugins: easy-server-0.5.0


.. _`Server file and vault file`:

Server file and vault file
--------------------------

The server file define the servers, server groups and a default
server or group. It is described in the "easy-server" documentation in section
`Server files <https://easy-server.readthedocs.io/en/stable/usage.html#server-files>`_.

The vault file defines the secrets needed to access the servers and can stay
encrypted in the file system while being used. It is described in the
"easy-server" documentation in section
`Vault files <https://easy-server.readthedocs.io/en/stable/usage.html#vault-files>`_.

The servers and groups are identified with user-defined nicknames.


.. _`Using the es_server fixture`:

Using the es_server fixture
---------------------------

If your pytest test function uses the :func:`~pytest_easy_server.es_server`
fixture, the test function will be invoked for the server specified in the
``--es-nickname`` command line option, or the set of servers if the specified
nickname is that of a server group.

From a perspective of the test function that is invoked, the fixture resolves
to a single server item.

The following example shows a test function using this fixture and how it gets
to the details for accessing the server:

.. code-block:: python

    from pytest_easy_server import es_server

    def test_sample(es_server):
        """
        Example Pytest test function that tests something.

        Parameters:
          es_server (easy_server.Server): Pytest fixture; the server to be
            used for the test
        """

        # Standard properties from the server file:
        nickname = es_server.nickname
        description = es_server.description

        # User-defined additional properties from the server file:
        stuff = es_server.user_defined['stuff']

        # User-defined secrets from the vault file:
        host = es_server.secrets['host']
        username = es_server.secrets['username']
        password = es_server.secrets['password']

        # Session to server using a fictitious session class
        session = MySession(host, username, password)

        # Test something
        result = my_session.perform_function()
        assert ...

        # Cleanup
        session.close()

The example shows how to access the standard and user-defined properties
from the "easy-server" file for demonstration purposes. The data structure
of the user-defined properties in the server file and of the secrets
in the vault file is completely up to you, so you could decide to have the host
and userid in user-defined properties in the server file, and have
only the password in the vault file.

The ``es_server`` parameter of the test function is a
:class:`easy_server:easy_server.Server` object that represents a
server item from the server file for testing against a single server. It
includes the corresponding secrets item from the vault file.


Example pytest runs
-------------------

The user-defined properties and vault secrets used in the test function shown
in the previous section are from the examples located in the ``examples``
directory of the
`GitHub repo of the project <https://github.com/andy-maier/pytest-easy-server/issues>`_.
The pytest runs are performed from within that directory.

Example file ``es_server.yml``:

.. code-block:: yaml

    vault_file: vault.yml

    servers:

      myserver1:                            # Nickname of the server
        description: "my dev system 1"
        contact_name: "John Doe"
        access_via: "VPN to dev network"
        user_defined:                       # User-defined additional properties
          stuff: "more stuff"

      myserver2:
        description: "my dev system 2"
        contact_name: "John Doe"
        access_via: "intranet"
        user_defined:
          stuff: "more stuff"

    server_groups:

      mygroup1:
        description: "my dev systems"
        members:
          - myserver1
          - myserver2

    default: mygroup1

Example file ``es_vault.yml``:

.. code-block:: yaml

    secrets:

      myserver1:
        host: "10.11.12.13"                 # User-defined properties
        username: myuser1
        password: mypass1

      myserver2:
        host: "9.10.11.12"                  # User-defined properties
        username: myuser2
        password: mypass2

The directory also contains a test module ``test_function.py`` with a test
function that uses the :func:`~pytest_easy_server.es_server` fixture and prints
the attributes and secrets for the server it is invoked for.

The following pytest runs use the default server file (``es_server.yml`` in the
current directory) and the vault password had been prompted for already and is
now found in the keyring service.

In pytest verbose mode, the **pytest-easy-server** plugin prints messages
about which server file is used and where the vault password comes from.

In this pytest run, the default nickname is used (the default defined in the
server file, which is group ``mygroup1`` that contains servers ``myserver1``
and ``myserver2``):

.. code-block:: text

    $ pytest -s -v .
    ==================================================== test session starts ====================================================
    platform darwin -- Python 3.8.7, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /Users/maiera/virtualenvs/pytest-es38/bin/python
    cachedir: .pytest_cache
    rootdir: /Users/maiera/PycharmProjects/pytest-easy-server
    plugins: easy-server-0.5.0.dev1
    collecting ...
    pytest-easy-server: Using server file /Users/maiera/PycharmProjects/pytest-easy-server/examples/es_server.yml
    pytest-easy-server: Using vault password from prompt or keyring service.
    collected 2 items

    test_function.py::test_sample[es_server=myserver1]
    MySession: host=10.11.12.13, username=myuser1, password=mypass1
    PASSED
    test_function.py::test_sample[es_server=myserver2]
    MySession: host=9.10.11.12, username=myuser2, password=mypass2
    PASSED

    ===================================================== 2 passed in 0.02s =====================================================

In this pytest run, the nickname is specified in the pytest command line using
the ``--es-nickname`` option, to run only on server ``myserver1``:

.. code-block:: text

    $ pytest -s -v . --es-nickname myserver1
    ==================================================== test session starts ====================================================
    platform darwin -- Python 3.8.7, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /Users/maiera/virtualenvs/pytest-es38/bin/python
    cachedir: .pytest_cache
    rootdir: /Users/maiera/PycharmProjects/pytest-easy-server
    plugins: easy-server-0.5.0.dev1
    collecting ...
    pytest-easy-server: Using server file /Users/maiera/PycharmProjects/pytest-easy-server/examples/es_server.yml
    pytest-easy-server: Using vault password from prompt or keyring service.
    collected 1 item

    test_function.py::test_sample[es_server=myserver1]
    MySession: host=10.11.12.13, username=myuser1, password=mypass1
    PASSED

    ===================================================== 1 passed in 0.02s =====================================================


.. _`Controlling which servers to test against`:

Controlling which servers to test against
-----------------------------------------

When pytest loads the **pytest-easy-server** plugin, its set of command line
options gets extended by those contributed by the plugin. These options allow
controlling which server file is used and wich server or server
group is used to test against. These options are optional and have sensible
defaults:

.. code-block:: text

    --es-file=FILE
                            Path name of the easy-server file to be used.
                            Default: es_server.yml in current directory.
    --es-nickname=NICKNAME
                            Nickname of the server or server group to test against.
                            Default: The default from the server file.


.. _`Running pytest as a developer`:

Running pytest as a developer
-----------------------------

When running pytest with the **pytest-easy-server** plugin on your local system,
you are prompted (in the command line) for the vault password upon first use of
a particular vault file. The password is then stored in the keyring service of
your local system to avoid future such prompts.

The section :ref:`Running pytest in a CI/CD system` describes the use of
an environment variable to store the password which avoids the password prompt.
For security reasons, you should not use this approach when you run pytest
locally. The one password prompt can be afforded, and subsequent retrieval of
the vault password from the keyring service avoids further prompts.


.. _`Running pytest in a CI/CD system`:

Running pytest in a CI/CD system
--------------------------------

When running pytest with the **pytest-easy-server** plugin in a CI/CD system,
you must set an environment variable named "ES_VAULT_PASSWORD" to the vault
password.

This can be done in a secure way by defining a corresponding secret in the
CI/CD system in your test run configuration (e.g. GitHub Actions workflow),
and by setting that environment variable to the CI/CD system secret.

Here is a snippet from a GitHub Actions workflow that does that, using a
secret that is also named "ES_VAULT_PASSWORD":

.. code-block:: yaml

    - name: Run test
      env:
        ES_VAULT_PASSWORD: ${{ secrets.ES_VAULT_PASSWORD }}
      run: |
        pytest -s -v test_dir

The **pytest-easy-server** plugin picks up the vault password from the
"ES_VAULT_PASSWORD" environment variable if set and the presence of that
variable causes it not to prompt for the password and also not to store it in
the keyring service (which would be useless since it is on the system that is
used for the test run in the CI/CD system, and that is typically a new one for
every run).


.. _`Security aspects`:

Security aspects
----------------

There are two kinds of secrets involved:

* The secrets in the vault file.
* The vault password.

The secrets in the vault file are protected if the vault file is encrypted in
the file system. The functionality also works if the vault file is not
encrypted, but the normal case should be that you keep it encrypted. If you
store the vault file in a repository, make sure it is encrypted.

The vault password is protected in the following ways:

* When running pytest with the **pytest-easy-server** plugin on your local
  system, there is no permanent storage of the vault password anywhere except
  in the keyring service of your local system. There are no commands that take
  the vault password in their command line. The way the password gets specified
  is only in a password prompt, and then it is immediately stored in the keyring
  service and in future pytest runs retrieved from there.

  Your Python test programs of course can get at the secrets from the vault
  file (that is the whole idea after all). They can also get at the vault
  password by using the keyring service access functions but they have no need
  to deal with the vault password. In any case, make sure that the test
  functions do not print or log the vault secrets (or the vault password).

* When running pytest in a CI/CD system, the "ES_VAULT_PASSWORD" environment
  variable that needs to be set can be set from a secret stored in the CI/CD
  system. State of the art CI/CD systems go a long way of ensuring that
  these secrets cannot simply be echoed or otherwise revealed.

The keyring service provides access to the secrets stored there, for the user
that is authorized to access it. The details on how this is done depend on
the particular keyring service used and its configuration. For example,
on macOS the keyring service periodically requires re-authentication.


.. _`Derived Pytest fixtures`:

Derived Pytest fixtures
-----------------------

If using the :func:`~pytest_easy_server.es_server` fixture in your test
functions repeats boiler plate code for opening a session with the server,
this can be put into a derived fixture.

The following fixture is an example for that. It opens and closes a session
with a server using a fictitious class ``MySession``:

In a file ``session_fixture.py``:

.. code-block:: python

    import pytest
    from pytest_easy_server import es_server

    @pytest.fixture(scope='module')
    def my_session(request, es_server):
        """
        Pytest fixture representing the set of MySession objects to use for
        testing against a server.
        """
        # Session to server using a fictitious session class
        session = MySession(
            host=es_server.secrets['host']
            username=es_server.secrets['username']
            password=es_server.secrets['password']
        )

        yield session

        # Cleanup
        session.close()

In your test functions, you can now use that fixture:

.. code-block:: python

    from pytest_easy_server import es_server  # Must still be imported
    from session_fixture import my_session

    def test_sample(my_session):
        """
        Example Pytest test function that tests something.

        Parameters:
          my_session (MySession): Pytest fixture; the session to the server
            to be used for the test
        """
        result = my_session.perform_function()  # Test something

A side note: Pylint and Flake8 do not recognize that 'es_server' and 'my_session'
are fixtures that are interpreted by Pytest and thus complain about the unused
'es_server' and 'my_session' names, and about the 'my_session' parameter that
redefines the global name. The following markup silences these tools:

.. code-block:: python

    # pylint: disable=unused-import
    from pytest_easy_server import es_server  # noqa: F401
    from session_fixture import my_session  # noqa: F401

    def test_sample(my_session):  # pylint: disable=redefined-outer-name
