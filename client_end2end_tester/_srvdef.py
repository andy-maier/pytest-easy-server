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
Encapsulation of a single server definition.
"""

from __future__ import absolute_import, print_function

__all__ = ['ServerDefinition']


class ServerDefinition(object):
    """
    Encapsulation of a server definition (e.g. from a server definition file).
    """

    def __init__(self, nickname, server_dict):
        self._nickname = nickname
        self._description = server_dict['description']
        self._contact_name = server_dict.get('contact_name', None)
        self._access_via = server_dict.get('access_via', None)
        self._details = server_dict['details']

    def __repr__(self):
        return "ServerDefinition(" \
            "nickname={s._nickname!r}, " \
            "description={s._description!r}, " \
            "contact_name={s._contact_name!r}, " \
            "access_via={s._access_via!r}, " \
            "details={s._details!r})". \
            format(s=self)

    @property
    def nickname(self):
        """
        Nickname of the server.
        """
        return self._nickname

    @property
    def description(self):
        """
        Short description of the server.
        """
        return self._description

    @property
    def contact_name(self):
        """
        Name of technical contact for the server.
        """
        return self._contact_name

    @property
    def access_via(self):
        """
        Short reminder on the network/firewall/proxy/vpn used to access the
        server.
        """
        return self._access_via

    @property
    def details(self):
        """
        Details of the server, such as IP address.

        This object can have an arbitrary user-defined structure.
        """
        return self._details
