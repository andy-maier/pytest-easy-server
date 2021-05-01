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

The **pytest-easy-server** package is a `Pytest`_ plugin that provides a
`Pytest fixture`_ fixture :func:`~pytest_easy_server.es_server` that resolves
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


.. toctree::
   :maxdepth: 2
   :numbered:

   usage.rst
   api.rst
   development.rst
   appendix.rst
   changes.rst


.. # Links to documentation:

.. _`Pytest`: https://docs.pytest.org/en/stable/
.. _`Pytest fixture`: https://docs.pytest.org/en/stable/fixture.html
.. _`easy-server package`: https://easy-server.readthedocs.io/en/stable/
