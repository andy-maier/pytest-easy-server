# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pytest plugin.
"""

from __future__ import absolute_import, print_function
import os
import pytest

from ._exceptions import ServerDefinitionFileException
from ._srvdef import ServerDefinition
from ._srvdeffile import ServerDefinitionFile


def pytest_addoption(parser):
    """
    Add command line options and config (ini) parameters for this plugin.

    group.addoption() supports the same arguments as argparse.add_argument().
    """

    group = parser.getgroup('pytest-tars-plugin')
    group.description = "pytest-tars-plugin - " \
        "Pytest plugin for testing against real servers"

    group.addoption(
        '--cet-file',
        dest='cet_file',
        metavar="FILE",
        action='store',
        default=ServerDefinitionFile.default_filepath,
        help="""\
Use the specified server definition file.
Default: {fp} in current directory.
""".format(fp=ServerDefinitionFile.default_filepath))

    group.addoption(
        '--cet-server',
        dest='cet_server',
        metavar="NICKNAME",
        action='store',
        default=None,
        help="""\
Use the server or server group with this nickname to test against.
Default: default server or server group specified in the file.
""")


def fixtureid_server_definition(fixture_value):
    """
    Return a fixture ID to be used by pytest for fixture `server_definition()`.

    Parameters:

      fixture_value (:class:`~pytest_tars_plugin.ServerDefinition`):
        The server definition the test runs against.
    """
    sd = fixture_value
    assert isinstance(sd, ServerDefinition)
    return "server_definition={0}".format(sd.nickname)


def pytest_generate_tests(metafunc):
    """
    Pytest plugin function to generate the tests for multiple servers in the
    server definition file.
    """

    if 'server_definition' in metafunc.fixturenames:

        config = metafunc.config
        cet_file = os.path.abspath(config.getvalue('cet_file'))
        cet_server = config.getvalue('cet_server')

        if config.getvalue('verbose'):
            print("\npytest-tars-plugin: Loading server definition file: {}".
                  format(cet_file))

        # The following construct places the pytest.exit() call outside of the
        # exception handling which avoids the well-known exception traceback
        # "During handling of the above exception, ...".
        exit_message = None
        try:
            sdf = ServerDefinitionFile(cet_file)
        except ServerDefinitionFileException as exc:
            exit_message = str(exc)
        if exit_message:
            pytest.exit(exit_message)

        exit_message = None
        try:
            sd_list = sdf.list_default_servers() if cet_server is None else \
                sdf.list_servers(cet_server)
        except KeyError as exc:
            exit_message = str(exc)
        if exit_message:
            pytest.exit(exit_message)

        metafunc.parametrize(
            'server_definition', sd_list, indirect=True,
            ids=fixtureid_server_definition)
