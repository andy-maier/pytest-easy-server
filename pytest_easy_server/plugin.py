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
Pytest plugin for pytest-easy-server project.
"""

from __future__ import absolute_import, print_function
import os
import pytest

import easy_server

DEFAULT_SERVER_FILE = 'server.yml'
DEFAULT_VAULT_FILE = 'vault.yml'


def pytest_addoption(parser):
    """
    Add command line options and config (ini) parameters for this plugin.

    group.addoption() supports the same arguments as argparse.add_argument().
    """

    group = parser.getgroup('pytest-easy-server')
    group.description = "pytest-easy-server - " \
        "Pytest plugin for testing against real servers"

    group.addoption(
        '--es-server-file',
        dest='server_file',
        metavar="FILE",
        action='store',
        default=DEFAULT_SERVER_FILE,
        help="""\
Use the specified server definition file.
Default: {fn} in current directory.
""".format(fn=DEFAULT_SERVER_FILE))

    group.addoption(
        '--es-vault-file',
        dest='vault_file',
        metavar="FILE",
        action='store',
        default=DEFAULT_VAULT_FILE,
        help="""\
Use the specified vault file.
Default: {fn} in current directory.
""".format(fn=DEFAULT_VAULT_FILE))

    group.addoption(
        '--es-nickname',
        dest='nickname',
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

      fixture_value (:class:`~easy_server.ServerDefinition`):
        The server definition the test runs against.
    """
    sd = fixture_value
    assert isinstance(sd, easy_server.ServerDefinition)
    return "server_definition={0}".format(sd.nickname)


def pytest_generate_tests(metafunc):
    """
    Pytest plugin function to generate the tests for multiple servers in the
    server definition file.
    """

    if 'server_definition' in metafunc.fixturenames:

        config = metafunc.config
        server_file = os.path.abspath(config.getvalue('server_file'))
        vault_file = os.path.abspath(config.getvalue('vault_file'))
        nickname = config.getvalue('nickname')

        if config.getvalue('verbose'):
            print("\npytest-easy-server: Using server definition file {sfn} "
                  "and vault file {vfn}".
                  format(sfn=server_file, vfn=vault_file))

        # The following constructs place the pytest.exit() call outside of the
        # exception handling which avoids the well-known exception traceback
        # "During handling of the above exception, ...".

        exit_message = None
        try:
            sdf = easy_server.ServerDefinitionFile(server_file)
        except easy_server.ServerDefinitionFileException as exc:
            exit_message = str(exc)
        if exit_message:
            pytest.exit(exit_message)

        exit_message = None
        try:
            sd_list = sdf.list_default_servers() if nickname is None else \
                sdf.list_servers(nickname)
        except KeyError as exc:
            exit_message = str(exc)
        if exit_message:
            pytest.exit(exit_message)

        metafunc.parametrize(
            'server_definition', sd_list, indirect=True,
            ids=fixtureid_server_definition)
