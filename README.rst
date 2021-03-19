pytest-tars - Pytest plugin for testing against real servers
============================================================

.. image:: https://badge.fury.io/py/pytest-tars.svg
    :target: https://pypi.python.org/pypi/pytest-tars/
    :alt: Version on Pypi

.. image:: https://github.com/andy-maier/pytest-tars/workflows/test/badge.svg?branch=master
    :target: https://github.com/andy-maier/pytest-tars/actions/
    :alt: Actions status

.. image:: https://readthedocs.org/projects/pytest-tars/badge/?version=latest
    :target: https://readthedocs.org/projects/pytest-tars/builds/
    :alt: Docs build status (master)

.. image:: https://coveralls.io/repos/github/andy-maier/pytest-tars/badge.svg?branch=master
    :target: https://coveralls.io/github/andy-maier/pytest-tars?branch=master
    :alt: Test coverage (master)


.. _`Overview`:

Overview
--------

The pytest-tars package is a pytest plugin that provides support for
defining information about servers in a *server definition file* and using that
information via a pytest fixture in pytest test functions, so that the test
functions are called for all the servers that are specified.

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

The pytest fixture `server_definition`_ is used
in your tests as follows (assuming the server definition file has the
user-defined structure shown above):

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
`ServerDefinition`_ object that encapsulates the
server definition that is to be used for the test. Pytest will invoke the test
function repeatedly for all servers that are to be used for testing.

You can also build your own pytest fixtures on top of this one that provide for
example an open session with the server so that your test functions can
use the open session directly. That basically moves repeated boiler plate
code from your test functions into that fixture. Section
`Derived pytest fixtures`_ explains that in more detail.

Last but not least, the server definition file to be used and the server
or server group to be used for testing can be controlled with command line
options when invoking pytest:

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

  When pytest runs, it will automatically find the plugin and will show
  its version, e.g.:

  .. code-block:: text

      plugins: tars-0.5.0


.. _`Documentation`:

Documentation
------------

* `Documentation on RTD`_


License
-------

The pytest-tars project is provided under the
`Apache Software License 2.0 <https://raw.githubusercontent.com/andy-maier/pytest-tars/master/LICENSE>`_.


.. # Links to documentation:

.. _`Format of server definition file`: https://pytest-tars.readthedocs.io/en/latest/usage.html#format-of-server-definition-file
.. _`Protecting secrets`: https://pytest-tars.readthedocs.io/en/latest/usage.html#protecting-secrets
.. _`Derived pytest fixtures`: https://pytest-tars.readthedocs.io/en/latest/usage.html#derived-pytest-fixtures
.. _`server_definition`: https://pytest-tars.readthedocs.io/en/latest/api.html#server-definition-fixture
.. _`ServerDefinition`: https://pytest-tars.readthedocs.io/en/latest/api.html#serverdefinition-class
.. _`Documentation on RTD`: https://pytest-tars.readthedocs.io/en/latest/
