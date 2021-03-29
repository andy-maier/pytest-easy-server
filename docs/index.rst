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


pytest-easy-server - Pytest plugin for testing against real servers
*******************************************************************

The **pytest-easy-server** package is a `Pytest`_ plugin that provides a
`Pytest fixture`_ named :func:`~pytest_easy_server.server_definition` that
resolves to the set of servers the tests should run against.

The set of servers is defined in a *server definition file* and the secrets
to access the servers are defined in a *vault file*.

.. toctree::
   :maxdepth: 2
   :numbered:

   intro.rst
   usage.rst
   api.rst
   development.rst
   appendix.rst
   changes.rst

.. # Links to documentation:

.. _`Pytest`: https://docs.pytest.org/en/stable/
.. _`Pytest fixture`: https://docs.pytest.org/en/stable/fixture.html
