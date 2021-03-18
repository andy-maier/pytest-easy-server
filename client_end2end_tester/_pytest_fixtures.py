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
Pytest fixtures for server definitions.
"""

from __future__ import absolute_import, print_function
import os
import pytest

from ._srvdef import ServerDefinition
from ._srvdeffile import ServerDefinitionFile

__all__ = ['server_definition']

# Pick up server/group nickname from environment
TESTSERVER = os.getenv('TESTSERVER', 'default')

# Pick up server definition file from environment
TESTSERVERFILE = os.getenv('TESTSERVERFILE',
                           ServerDefinitionFile.default_filepath)

SDF = ServerDefinitionFile(TESTSERVERFILE)
SD_LIST = SDF.list_default_servers() if TESTSERVER == 'default' else \
    SDF.list_servers(TESTSERVER)


def fixtureid_server_definition(fixture_value):
    """
    Return a fixture ID to be used by pytest for fixture `server_definition()`.

    Parameters:
      * fixture_value (ServerDefinition): The server definition the test runs
        against.
    """
    sd = fixture_value
    assert isinstance(sd, ServerDefinition)
    return "server_definition={0}".format(sd.nickname)


@pytest.fixture(
    params=SD_LIST,
    scope='module',
    ids=fixtureid_server_definition
)
def server_definition(request):
    """
    Pytest fixture representing the set of server definitions for all servers
    to test against.

    Returns:
      ServerDefinition: Server definition for each server to test against.
    """
    return request.param
