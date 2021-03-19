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

This section describes the usage of the pytest-tars package.


.. _`Using the server_definition fixture`:

Using the server_definition fixture
-----------------------------------

The main purpose of the pytest-tars package is to provide the pytest fixture
:func:`~pytest_tars.server_definition` for use in your pytest testcases.

That fixture is used in your tests as follows:

.. code-block:: python

    from pytest_tars import server_definition

    def test_sample(server_definition):
        """
        Example pytest test function that tests something.

        Parameters:
          server_definition (ServerDefinition): Server to be used for the test
        """
        server_host = server_definition.details['host']
        server_userid = server_definition.details['userid']
        server_password = server_definition.details['password']
        # log on to the host and perform some test

The ``server_definition`` parameter of the test function is a
:class:`~pytest_tars.ServerDefinition` object that encapsulates the
server definition that is to be used for the test. Pytest will invoke the test
function repeatedly for all servers that are to be used for testing.

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
      myserver1:                   # nickname of the server
        description: "my dev system 1"
        contact_name: "John Doe"
        access_via: "VPN to dev network"
        details:                   # user-defined part, completely flexible
          host: "10.11.12.13"
          userid: myuserid
          password: mypassword


.. _`Format of server definition file`:

Format of server definition file
--------------------------------

The server definition file is in YAML format. Here is a working example:

.. code-block:: yaml

    servers:

      myserver1:                      # nickname of the server
        description: "my dev system 1"
        contact_name: "John Doe"
        access_via: "VPN to dev network"
        details:                      # user-defined part, completely flexible
          host: "10.11.12.13"
          userid: myuserid
          password: mypassword
          stuff:
            - morestuff1

      myserver2:                      # nickname of the server
        description: "my dev system 2"
        contact_name: "John Doe"
        access_via: "Company Intranet"
        details:                      # user-defined part, completely flexible
          host: "9.10.11.12"
          userid: myuserid
          password: mypassword

    server_groups:

      mygroup1:                       # nickname of the server group
        description: "my dev systems"
        members:                      # list of server or group nicknames
          - myserver1
          - myserver2

    default: mygroup1                 # nickname of default server or group

In the example above, ``myserver1``, ``myserver2``, and ``mygroup1`` are
nicknames of the respective server or server group definitions. These nicknames
are used when servers or groups are put into a server group in that file, or
when they are specified as a default in that file, or when they are used in the
``--cet-server`` command line option of pytest.

These nicknames are case sensitive and their allowable character set are
alphenumeric characters and the underscore character.

If tests are to be run against multiple servers in a single pytest invocation,
a corresponding server group needs to be defined in the file, and the server
group's nickname is specified to be used for testing (via default or the
``--cet-server`` option).

The value of the ``servers`` top-level property is an object (=dictionary) that
has one property for each server that is defined. The property name is the
server nickname, and the property value is an object with the following
properties. These propertes are accessible in the test function via same-named
properties of the :class:`~pytest_tars.ServerDefinition` object passed via the
fixture:

* ``description`` (string): Short description of the server (required).
* ``contact_name`` (string): Name of technical contact for the server (optional,
  defaults to `None`).
* ``access_via`` (string): Short reminder on the network/firewall/proxy/vpn
  used to access the server (optional, defaults to `None`).
* ``details`` (object): Details of the server, such as IP address. This object
  can have an arbitrary user-defined structure (required).

The value of the ``server_groups`` top-level property is an object that has one
property for each server group that is defined. The property name is the group
nickname, and the property value is an object with the following properties:

* ``description`` (string): Short description of the server group (required).
* ``members`` (list): List of server nicknames or other group nicknames that
  are the members of the group (required).

The value of the ``default`` top-level property is a string that is the
nickname of the default server or group to be used if the ``--cet-server``
command line option of pytest is not specified.

Servers may be put into multiple server groups.

Server groups may be put into server groups at arbitrary nesting depth, as long
as there is no infinite recursion anywhere.

When specifying a server group to be used for testing, the resulting set of
servers that is actually passed to the :func:`~pytest_tars.server_definition`
fixture is the flattened list of servers, whereby any duplicate servers are
eliminated.

The format of the server definition file is validated when pytest runs, and
pytest will stop with an error if validation issues are found.


.. _`Controlling which servers to test against`:

Controlling which servers to test against
-----------------------------------------

When pytest loads the pytest-tars plugin, its set of command line options
gets extended by those contributed by the plugin. These options allow
controlling which server definition file is used and wich server or server
group is used to test against. These options are optional and have sensible
defaults:

.. code-block:: text

    --cet-file=FILE       Use the specified server definition file.
                          Default: tars.yaml in current directory.

    --cet-server=NICKNAME
                          Use the server or server group with this nickname to test against.
                          Default: default server or server group specified in the file.


.. _`Protecting secrets`:

Protecting secrets
------------------

When the server definition file is placed in a repository, any server secrets
such as passwords, private keys, etc. should not be in that file in clear text
form. There are multiple ways how this can be done:

* Approach 1: Encrypt the server secrets and keep their encrypted form in the
  user-defined part of the server definition in the file.
  This requires a key for decrypting the server secrets that is put as a
  secret into the CI/CD system you use to run the tests, using its facilities
  for storing such secrets.

* Approach 2: Put the server secrets into a vault, and protect the vault
  with a CI/CD secret. The vault may be a file in your repository (such as
  an Ansible vault), or a vault service (such as Hashicorp Vault).

Example
^^^^^^^

The following example shows approach 2 using GitHub Actions as a CI/CD system
that runs your tests, and an Ansible vault file that is put into your
repository.

In the example, two servers are specified. Optional elements in the server
definition file are omitted, for simplicity.

You can find the files shown in this example in the
`examples/approach2 <https://github.com/andy-maier/pytest-tars/tree/master/examples/approach2>`_
directory of the repository.

* Create a server definition file named ``tars.yaml`` that specifies the
  servers with host and userid (but no password) in the user-defined part:

  .. code-block:: yaml

      servers:
        myserver1:
          description: "my dev system 1"
          details:
            host: "10.11.12.13"
            userid: myuserid1
        myserver2:
          description: "my dev system 2"
          details:
            host: "10.11.12.14"
            userid: myuserid2

* Create an Ansible vault file named ``vault.yaml`` that specifies the passwords
  for each server, using the server nicknames as keys:

  .. code-block:: yaml

      passwords:
        myserver1: mypass1
        myserver2: mypass2

* Encrypt the Ansible vault file before it is put into the repository:

  .. code-block:: bash

      $ ansible-vault encrypt vault.yaml
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
          command: "ansible-vault decrypt vault.yaml"

* Write a Python function that accesses the vault file and returns the password
  for a given nickname, a.g. in a module named ``utils.py``:

  .. code-block:: python

      def get_password(nickname):
          with open('vault.yaml', 'r') as fp:
              vault_dict = yaml.safe_load(fp)
          return vault_dict['passwords'][nickname]

* In each of your test functions, access the server host, userid and password
  as follows:

  .. code-block:: python

      from pytest_tars import server_definition
      from .utils import get_password

      def test_sample(server_definition):
          server_host = server_definition.details['host']
          server_userid = server_definition.details['userid']
          server_password = get_password(server_definition.nickname)
          # log on to the host and perform some test


.. _`Derived pytest fixtures`:

Derived pytest fixtures
-----------------------

If using the server definition in your test functions includes the same boiler
plate code for opening a session with the server, this can be put into a
second fixture. For example, the following fixture opens and closes a
session with a server using a fictitious class ``MySession``, and the
approach 2 for storing secrets described in the previous section:

In a file ``session_fixture.py``:

.. code-block:: python

    import pytest
    from pytest_tars import server_definition
    from .utils import get_password

    @pytest.fixture(scope='module')
    def my_session(request, server_definition):
        """
        Pytest fixture representing the set of MySession objects to use for
        testing against a server.
        """
        session = MySession(
            host = server_definition.details['host']
            userid = server_definition.details['userid']
            password = get_password(server_definition.nickname)
        )
        yield session
        session.close()

In your test functions, you can now use that fixture:

.. code-block:: python

    from pytest_tars import server_definition  # Must still be imported
    from session_fixture import my_session

    def test_sample(my_session):
        result = my_session.perform_function()  # Test something
