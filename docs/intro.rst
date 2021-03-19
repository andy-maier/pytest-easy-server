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

.. contents:: Chapter Contents
   :depth: 2


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
a server definition file. Section :ref:`Format of server definition file`
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
or references some vault containing them. Section :ref:`Protecting secrets`
explains that in more detail.

The pytest fixture :func:`~pytest_tars.server_definition` is used
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
:class:`~pytest_tars.ServerDefinition` object that encapsulates the
server definition that is to be used for the test. Pytest will invoke the test
function repeatedly for all servers that are to be used for testing.

You can also build your own pytest fixtures on top of this one that provide for
example an open session with the server so that your test functions can
use the open session directly. That basically moves repeated boiler plate
code from your test functions into that fixture. Section
:ref:`Derived pytest fixtures` explains that in more detail.

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
