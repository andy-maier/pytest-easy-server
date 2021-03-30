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


pytest-easy-server - Pytest plugin for easy testing against servers
*******************************************************************

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


.. toctree::
   :maxdepth: 2
   :numbered:

   usage.rst
   api.rst
   development.rst
   appendix.rst
   changes.rst
