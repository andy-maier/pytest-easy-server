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
Test the _easy_server_fixture.py module.
"""

from __future__ import absolute_import, print_function
import pytest
import easy_server

# pylint: disable=unused-import
from pytest_easy_server import es_server  # noqa: F401


@pytest.mark.parametrize(
    "num",
    [1, 2]
)
# pylint: disable=redefined-outer-name
def test_fixture_sample(es_server, num):
    """
    Sample test using the es_server fixture.

    The server file used for this test is specified in the pytest
    invocation in the Makefile. The file is expected to be the es_server.yml
    file in the unittest directory. It specifies the es_vault.yml file as
    a vault file.

    Parameters:
      es_server (easy_server.Server): A server item
    """
    assert isinstance(es_server, easy_server.Server)

    # This test uses the default server file, so we expect the
    # default servers defined in that file:
    exp_nicks = ['myserver1', 'myserver2']
    exp_servers = {
        'myserver1': dict(
            description="my dev system 1",
            contact_name="John Doe",
            access_via="VPN to dev network",
            user_defined=dict(
                stuff="more stuff",
            ),
            secrets=dict(
                host='10.11.12.13',
                username='myuser1',
                password='mypass1',
            ),
        ),
        'myserver2': dict(
            description="my dev system 2",
            contact_name="John Doe",
            access_via="intranet",
            user_defined=dict(
                stuff="more stuff",
            ),
            secrets=dict(
                host='9.10.11.12',
                username='myuser2',
                password='mypass2',
            ),
        ),
    }

    assert num in (1, 2)
    assert es_server.nickname in exp_nicks

    nick = es_server.nickname
    assert es_server.description == exp_servers[nick]['description']
    assert es_server.contact_name == exp_servers[nick]['contact_name']
    assert es_server.access_via == exp_servers[nick]['access_via']
    assert es_server.user_defined == exp_servers[nick]['user_defined']
    assert es_server.secrets == exp_servers[nick]['secrets']
