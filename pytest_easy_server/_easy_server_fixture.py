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
Pytest fixture es_server.
"""

from __future__ import absolute_import, print_function
import pytest

import easy_server

__all__ = ['es_server']


@pytest.fixture(scope="module")
def es_server(request):
    """
    Pytest fixture representing a server item from an 'easy-server' file as a
    :class:`easy_server:easy_server.Server` object.

    Pytest invokes testcases using this fixture for all servers to test against.

    The servers are defined in a :ref:`Server file and vault file`.
    The servers to test against are controlled with pytest command line options
    as described in :ref:`Controlling which servers to test against`.

    Returns:
      :class:`easy_server:easy_server.Server`:
      Server item for each server to test against.
    """
    es_obj = request.param
    assert isinstance(es_obj, easy_server.Server)
    return es_obj
