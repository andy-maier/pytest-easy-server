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


pytest-tars - Pytest plugin for testing against real servers
************************************************************

The pytest-tars package ("tars" = testing against real servers) is a `Pytest`_
plugin that provides support for defining information about how to access
servers (including a flexible user-defined part) in a *server definition file*
and a `Pytest fixture`_ named :func:`~pytest_tars.server_definition` so that a
Pytest testcase using that fixture can test against a server or group of servers
defined in that file.

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
