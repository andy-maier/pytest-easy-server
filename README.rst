client_end2end_tester - Testing Python client libraries against real servers
============================================================================

.. image:: https://badge.fury.io/py/client_end2end_tester.svg
    :target: https://pypi.python.org/pypi/client_end2end_tester/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/client_end2end_tester/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/client_end2end_tester/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/client_end2end_tester/badge/?version=latest
    :target: https://readthedocs.org/projects/client_end2end_tester/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/client_end2end_tester/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/client_end2end_tester?branch=master
    :alt: Test coverage (master)


.. _`Overview`:

Overview
--------

The client_end2end_tester package provides support for defining information
about servers in a *server definition file* and using that information in
pytest fixtures, so that the pytest testcase is run against all the servers
that are specified.

The server definition file is in YAML format and allows defining servers,
grouping them into server groups, and defining a default server or group.

The information that can be defined for a server has a standard part and
a completely flexible user-defined part, as shown in this example of
a server definition file. Section `Format of server definition file`_
explains the format in more detail.

Example server definition file:

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
          stuff:
            - morestuff1

    server_groups:

      mygroup1:                    # nickname of the server group
        description: "my dev systems"
        members:
          - myserver1

    default: mygroup1    # nickname of default server or group

If you want to put the server definition file into a repository, you do not
want to have any passwords or other secrets in there, and in that case you
can define the user-defined part such that it either encrypts these secrets,
or references some vault containing them. Section `Protecting secrets`_
explains that in more detail.

The pytest fixture `server_definition`_ can be used
in your tests as follows (assuming the server definition file has the
user-defined structure shown above):

.. code-block:: python

    from client_end2end_tester import server_definition

    def test_sample1(server_definition):
        """
        Example pytest test function that tests something.

        Parameters:
          server_definition (ServerDefinition): Server to be used for the test
        """
        server_host = server_definition.details['host']
        server_userid = server_definition.details['userid']
        server_password = server_definition.details['password']
        # log on to the host and perform some test

The ``server_definition`` parameter of the fixture is a
`ServerDefinition`_ object that encapsulates the
server definition that is to be used for the test. Pytest will invoke the test
function repeatedly for all servers that are to be used for testing.

You can also build your own pytest fixtures on top of this one that provide for
example an open session with the server so that your test functions can
use the open session directly. That basically moves repeated boiler plate
code from your test functions into that fixture. Section
`Derived pytest fixtures`_ explains that in more detail.

Last but not least, the server definition file to be used and the server
or server group to be used for testing can be controlled with two environment
variables:

.. code-block:: shell

    # Server definition file to be used.
    # If not specified, defaults to 'server_definition_file.yaml' in the
    # current directory.
    export TESTSERVERFILE=server_definition_file.yaml

    # Nickname of the server or server group to be used.
    # If not specified, defaults to the default server or group in the file.
    export TESTSERVER=mygroup1


.. _`Supported environments`:

Supported environments
----------------------

client_end2end_tester is supported in these environments:

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

* Install the client_end2end_tester package and its prerequisite
  Python packages into the active Python environment:

  .. code-block:: bash

      $ pip install client_end2end_tester


.. _`Documentation`:

Documentation
------------

* `Documentation`_


License
-------

The client_end2end_tester project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/client_end2end_tester/master/LICENSE>`_.


.. # Links to documentation:

.. _`Format of server definition file`: https://client-end2end-tester.readthedocs.io/en/latest/usage.html#format-of-server-definition-file
.. _`Protecting secrets`: https://client-end2end-tester.readthedocs.io/en/latest/usage.html#protecting-secrets
.. _`Derived pytest fixtures`: https://client-end2end-tester.readthedocs.io/en/latest/usage.html#derived-pytest-fixtures
.. _`server_definition`: https://client-end2end-tester.readthedocs.io/en/latest/api.html#server-definition-fixture
.. _`ServerDefinition`: https://client-end2end-tester.readthedocs.io/en/latest/api.html#serverdefinition-class
.. _`Documentation`: https://client-end2end-tester.readthedocs.io/en/latest/
