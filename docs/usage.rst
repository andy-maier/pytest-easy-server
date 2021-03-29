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

pytest-easy-server is supported in these environments:

* Operating Systems: Linux, Windows (native, and with UNIX-like environments),
  macOS/OS-X

* Python: 2.7, 3.4, and higher


.. _`Installation`:

Installation
------------

* Prerequisites:

  - The Python environment into which you want to install must be the current
    Python environment, and must have at least the following Python packages
    installed:

    - setuptools
    - wheel
    - pip

* Install the pytest-easy-server package and its prerequisite
  Python packages into the active Python environment:

  .. code-block:: bash

      $ pip install pytest-easy-server

  When Pytest runs, it will automatically find the plugin and will show
  its version, e.g.:

  .. code-block:: text

      plugins: easy-server-0.5.0


.. _`Using the server_definition fixture`:

Using the server_definition fixture
-----------------------------------

The main purpose of the pytest-easy-server package is to provide the Pytest fixture
:func:`~pytest_easy_server.server_definition` for use in your Pytest testcases.

That fixture is used in your tests as follows:

.. code-block:: python

    from pytest_easy_server import server_definition

    def test_sample(server_definition):
        """
        Example Pytest test function that tests something.

        Parameters:
          server_definition (ServerDefinition): Server to be used for the test
        """
        server_host = server_definition.user_defined['host']
        server_username = server_definition.user_defined['username']
        server_password = server_definition.user_defined['password']
        # log on to the host and perform some test

The ``server_definition`` parameter of the test function is the use of the
Pytest fixture. This fixture parameter resolves to a
:class:`~pytest_easy_server.ServerDefinition` object that represents a server
definition from the file for test of a single server.  Pytest will invoke the
test function for all servers that are to be tested.

This test function relies on certain elements in the user-defined part of
the server definition in your server definition file, such as the hostname
or IP address of the server, and credentials to log on.

The structure of these user-defined elements is completely up to you: You
simply define these elements in your server definition file, and use them in
your test functions.

An example server definition file that corresponds to the test function shown
above would be:

.. code-block:: yaml

    servers:
      myserver1:                          # nickname of the server
        description: "my dev system 1"
        contact_name: "John Doe"
        access_via: "VPN to dev network"
        user_defined:                     # user-defined part, completely flexible
          host: "10.11.12.13"
          username: myusername
          password: mypassword


.. _`Format of server definition file`:

Format of server definition file
--------------------------------

The server definition file is in YAML format. Here is a working example:

.. code-block:: yaml

    servers:

      myserver1:                          # nickname of the server
        description: "my dev system 1"
        contact_name: "John Doe"
        access_via: "VPN to dev network"
        user_defined:                     # user-defined part, completely flexible
          host: "10.11.12.13"
          username: myusername
          password: mypassword
          stuff:
            - morestuff1

      myserver2:                          # nickname of the server
        description: "my dev system 2"
        contact_name: "John Doe"
        access_via: "Company Intranet"
        user_defined:                     # user-defined part, completely flexible
          host: "9.10.11.12"
          username: myusername
          password: mypassword

    server_groups:

      mygroup1:                           # nickname of the server group
        description: "my dev systems"
        members:                          # list of server or group nicknames
          - myserver1
          - myserver2

    default: mygroup1                     # nickname of default server or group

In the example above, ``myserver1``, ``myserver2``, and ``mygroup1`` are
nicknames of the respective server or server group definitions. These nicknames
are used when servers or groups are put into a server group in that file, or
when they are specified as a default in that file, or when they are used in the
``--es-nickname`` command line option of the pytest command.

These nicknames are case sensitive and their allowable character set are
alphenumeric characters and the underscore character.

If tests are to be run against multiple servers in a single pytest invocation,
a corresponding server group needs to be defined in the file, and the server
group's nickname is specified to be used for testing (via default or the
``--es-nickname`` option).

The value of the ``servers`` top-level property is an object (=dictionary) that
has one property for each server that is defined. The property name is the
server nickname, and the property value is an object with the following
properties. These propertes are accessible in the test function via same-named
properties of the :class:`~pytest_easy_server.ServerDefinition` object passed via the
fixture:

* ``description`` (string): Short description of the server (required).
* ``contact_name`` (string): Name of technical contact for the server (optional,
  defaults to `None`).
* ``access_via`` (string): Short reminder on the network/firewall/proxy/vpn
  used to access the server (optional, defaults to `None`).
* ``user_defined`` (object): Details of the server, such as IP address. This object
  can have an arbitrary user-defined structure (required).

The value of the ``server_groups`` top-level property is an object that has one
property for each server group that is defined. The property name is the group
nickname, and the property value is an object with the following properties:

* ``description`` (string): Short description of the server group (required).
* ``members`` (list): List of server nicknames or other group nicknames that
  are the members of the group (required).

The value of the ``default`` top-level property is a string that is the
nickname of the default server or group to be used if the ``--es-nickname``
command line option of pytest is not specified.

Server groups may be nested. That is, server groups may be put into other server
groups at arbitrary nesting depth. There must not be any cycle (i.e. the
resulting graph of server groups must be a tree).

A particular server or server group may be put into more than one server group.

When specifying a server group to be used for testing, the resulting set of
servers that is actually passed to the :func:`~pytest_easy_server.server_definition`
fixture is the flattened list of servers, whereby any duplicate servers are
eliminated.

The format of the server definition file is validated when pytest runs, and
pytest will stop with an error if validation issues are found.


.. _`Controlling which servers to test against`:

Controlling which servers to test against
-----------------------------------------

When pytest loads the pytest-easy-server plugin, its set of command line options
gets extended by those contributed by the plugin. These options allow
controlling which server definition file is used and wich server or server
group is used to test against. These options are optional and have sensible
defaults:

.. code-block:: text

    --es-server-file=FILE   Use the specified server definition file.
                            Default: server.yml in current directory.

    --es-vault-file=FILE    Use the specified vault file.
                            Default: vault.yml in current directory.

    --es-nickname=NICKNAME  Use the server or server group with this
                            nickname to test against.
                            Default: default server or server group
                            specified in the server definition file.


.. _`Protecting secrets`:

Protecting secrets
------------------

If the server definition file is stored in a repository, it should not contain
any passwords or other secrets in clear text. There are multiple ways how this
can be achieved:

* Approach 1: Encrypt the server secrets and keep their encrypted form in the
  user-defined part of the server definition in the file. This requires a key
  for decrypting the server secrets. Use the secret management facilities of
  the CI/CD system that runs the tests for storing the decryption key.

* Approach 2: Put the server secrets into a vault, and protect the vault
  with a CI/CD secret. The vault may be an encrypted file in your repository
  (such as an Ansible vault), or a vault service (such as Hashicorp Vault).
  Use the secret management facilities of the CI/CD system that runs the tests
  for storing the access data for the vault.

Example
^^^^^^^

The following example shows approach 2 using GitHub Actions as a CI/CD system
that runs your tests, and an Ansible vault file that is put into your
repository.

In the example, two servers are specified. Optional elements in the server
definition file are omitted, for simplicity.

You can find the files shown in this example in the
`examples/approach2 <https://github.com/andy-maier/pytest-easy-server/tree/master/examples/approach2>`_
directory of the repository.

* Create a server definition file named ``server.yml`` that specifies the
  servers with host and username (but no password) in the user-defined part:

  .. code-block:: yaml

      servers:
        myserver1:
          description: "my dev system 1"
          user_defined:
            host: "10.11.12.13"
            username: myusername1
        myserver2:
          description: "my dev system 2"
          user_defined:
            host: "10.11.12.14"
            username: myusername2

* Create an Ansible vault file named ``vault.yml`` that specifies the passwords
  for each server, using the server nicknames as keys:

  .. code-block:: yaml

      passwords:
        myserver1: mypass1
        myserver2: mypass2

* Encrypt the Ansible vault file before it is put into the repository:

  .. code-block:: bash

      $ ansible-vault encrypt vault.yml
      New Vault password: ......
      Confirm New Vault password: ......
      Encryption successful

* Create a secret in GitHub Actions for your repo, with name ``vault_password``
  and the vault password you just specified as its value. For details, see
  `GitHub Actions encrypted secrets <https://docs.github.com/en/actions/reference/encrypted-secrets>`_.

* Put the following step into your GitHub Actions test workflow before the
  step that runs pytest, to decrypt the vault file:

  .. code-block:: yaml

      - name: Decrypt the vault
        uses: anthonykgross/ansible-vault-cli-github-action@v1
        with:
          vault_key: ${{ secrets.vault_password }}
          command: "ansible-vault decrypt vault.yml"

* Write a Python function that accesses the vault file and returns the password
  for a given nickname, a.g. in a module named ``utils.py``:

  .. code-block:: python

      def get_password(nickname):
          with open('vault.yml', 'r') as fp:
              vault_dict = yaml.safe_load(fp)
          return vault_dict['passwords'][nickname]

* In each of your test functions, access the server host, username and password
  as follows:

  .. code-block:: python

      from pytest_easy_server import server_definition
      from .utils import get_password

      def test_sample(server_definition):
          server_host = server_definition.user_defined['host']
          server_username = server_definition.user_defined['username']
          server_password = get_password(server_definition.nickname)
          # log on to the host and perform some test


.. _`Derived Pytest fixtures`:

Derived Pytest fixtures
-----------------------

If using the server definition in your test functions includes the same boiler
plate code for opening a session with the server, this can be put into a
second fixture. For example, the following fixture opens and closes a
session with a server using a fictitious class ``MySession``, and the
approach 2 for storing secrets described in the previous section:

In a file ``session_fixture.py``:

.. code-block:: python

    import pytest
    from pytest_easy_server import server_definition
    from .utils import get_password

    @pytest.fixture(scope='module')
    def my_session(request, server_definition):
        """
        Pytest fixture representing the set of MySession objects to use for
        testing against a server.
        """
        session = MySession(
            host = server_definition.user_defined['host']
            username = server_definition.user_defined['username']
            password = get_password(server_definition.nickname)
        )
        yield session
        session.close()

In your test functions, you can now use that fixture:

.. code-block:: python

    from pytest_easy_server import server_definition  # Must still be imported
    from session_fixture import my_session

    def test_sample(my_session):
        result = my_session.perform_function()  # Test something
