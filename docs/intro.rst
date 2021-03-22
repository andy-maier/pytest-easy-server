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


.. _`Introduction`:

Introduction
============


.. _`Overview`:

Overview
--------

The pytest-tars package ("tars" = testing against real servers) is a `Pytest`_
plugin that provides support for defining information about how to access
servers (including a flexible user-defined part) in a *server definition file*
and a `Pytest fixture`_ named :func:`~pytest_tars.server_definition` so that a
Pytest testcase using that fixture can test against a server or group of servers
defined in that file.

The server definition file is in YAML format and allows defining servers,
grouping them into server groups, and defining a default server or group.

The information that can be defined for a server has a standard part and
a completely flexible user-defined part, as shown in this example of
a server definition file. Section :ref:`Format of server definition file`
explains the format in more detail.

Example server definition file:

.. code-block:: yaml

    servers:

      myserver1:                          # nickname of the server
        description: "my dev system 1"    # short description of server
        contact_name: "John Doe"          # optional: Contact for the server
        access_via: "VPN to dev network"  # optional: Any special network access needed
        user_defined:                     # user-defined part, completely flexible
          host: "10.11.12.13"
          username: myusername
          password: mypassword
          stuff:
            - morestuff1

    server_groups:

      mygroup1:                           # nickname of the server group
        description: "my dev systems"     # short description of server group
        members:                          # group members, using the nicknames
          - myserver1

    default: mygroup1                     # default server or group, using the nickname

If the server definition file is stored in a repository, it should not contain
any passwords or other secrets in clear text. To achieve that, you can for
example have encrypted versions of the secrets in the user-defined section, or
move the secrets to a vault. Section :ref:`Protecting secrets` explains that in
more detail.

The `Pytest fixture`_ :func:`~pytest_tars.server_definition` is used in your
tests as follows (assuming the server definition file defines user-defined
properties ``host``, ``username``, and ``password``):

.. code-block:: python

    from pytest_tars import server_definition

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
:class:`~pytest_tars.ServerDefinition` object that represents a server
definition from the file for test of a single server.  Pytest will invoke the
test function for all servers that are to be tested.

You can also build your own Pytest fixtures on top of the
:func:`~pytest_tars.server_definition` fixture. An example for that is a
fixture representing an open session with the server so that your test functions
can use the open session directly instead of having to create it every time.
That moves repeated boiler plate code from your test functions into your
fixture. Section :ref:`Derived Pytest fixtures` explains that in more detail.

The server definition file to be used and the server or server group to be used
for testing can be controlled with command line options when invoking the
pytest command:

.. code-block:: text

    --tars-file=FILE      Use the specified server definition file.
                          Default: tars.yaml in current directory.

    --tars-server=NICKNAME
                          Use the server or server group with this nickname to test against.
                          Default: default server or server group specified in the file.


.. _`Supported environments`:

Supported environments
----------------------

pytest-tars is supported in these environments:

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

* Install the pytest-tars package and its prerequisite
  Python packages into the active Python environment:

  .. code-block:: bash

      $ pip install pytest-tars

  When Pytest runs, it will automatically find the plugin and will show
  its version, e.g.:

  .. code-block:: text

      plugins: tars-0.5.0

.. # Links to documentation:

.. _`Pytest`: https://docs.pytest.org/en/stable/
.. _`Pytest fixture`: https://docs.pytest.org/en/stable/fixture.html
