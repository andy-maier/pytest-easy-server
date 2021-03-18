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
Encapsulation of server definition files.
"""

from __future__ import absolute_import, print_function
import yaml
import jsonschema

from ._srvdef import ServerDefinition

__all__ = ['ServerDefinitionFileNotFound', 'ServerDefinitionFileError',
           'ServerDefinitionFile']


# JSON schema describing the structure of the server definition files
SERVER_DEFINITION_FILE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "JSON schema for server definition files",
    "definitions": {},
    "type": "object",
    "required": [
        "servers",
    ],
    "additionalProperties": False,
    "properties": {
        "servers": {
            "type": "object",
            "description": "The servers in the server definition file",
            "additionalProperties": False,
            "patternProperties": {
                "^[a-zA-Z0-9_]+$": {
                    "type": "object",
                    "description": "Nickname of the server",
                    "required": [
                        "description",
                        "details",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Short description of the server",
                        },
                        "contact_name": {
                            "type": "string",
                            "description":
                                "Name of technical contact for the server",
                        },
                        "access_via": {
                            "type": "string",
                            "description":
                                "Short reminder on the "
                                "network/firewall/proxy/vpn used to access the "
                                "server",
                        },
                        "details": {
                            "type": "object",
                            "description":
                                "Details of the server, such as IP address. "
                                "This object can have an arbitrary "
                                "user-defined structure",
                        },
                    },
                },
            },
        },
        "server_groups": {
            "type": "object",
            "description": "The server groups in the server definition file",
            "additionalProperties": False,
            "patternProperties": {
                "^[a-zA-Z0-9_]+$": {
                    "type": "object",
                    "description": "Nickname of the server group",
                    "required": [
                        "description",
                        "members",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "description": {
                            "type": "string",
                            "description":
                                "Short description of the server group",
                        },
                        "members": {
                            "type": "array",
                            "description":
                                "List of members of the server group. "
                                "Those can be servers or other server groups.",
                            "items": {
                                "type": "string",
                                "description":
                                    "Nickname of server or server group in "
                                    "this file",
                            },
                        },
                    },
                },
            },
        },
        "default": {
            "type": "string",
            "description": "Nickname of default server or server group",
        },
    },
}


class ServerDefinitionFileNotFound(Exception):
    """
    Exception indicating that a server definition file was not found or cannot
    be accessed due to a permission error.
    """
    pass


class ServerDefinitionFileError(Exception):
    """
    Exception indicating that an existing server definition file has some
    issue with the format of its file content.
    """
    pass


class ServerDefinitionFile(object):
    """
    Encapsulates the access to a server definition file.

    This file defines servers for end2end tests of clients and has the following
    format:

        servers:                # Server definitions.
          SRV1:                 # Nickname of the server.
            description: TEXT   # Short description of the server.
            contact_name: TEXT  # Name of technical contact for the server.
            access_via: TEXT    # Short reminder on the network/firewall/proxy/
                                # vpn used to access the server.
            details:            # Details of the server, such as IP address.

        server_groups:          # Server groups.
          GRP1:                 # Nickname of server group.
            description: TEXT   # Short description of the server group.
            members:            # Members of the server group.
              - SRV1            # Nickname of a member (server or group).

        default: GRP1           # Default server or server group.
    """

    default_filepath = 'examples/server_definitions.yaml'

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = self.default_filepath
        self._filepath = filepath
        self._data = _load_validate_default(filepath)
        # The following attributes are for faster access
        self._servers = self._data['servers']
        self._server_groups = self._data['server_groups']
        self._default = self._data['default']

    @property
    def filepath(self):
        """
        string: File path of the server definition file.
        """
        return self._filepath

    def get_server(self, nickname):
        """
        Get server definition for a given server nickname.

        Parameters:
          nickname (string): Server nickname.

        Returns:
          class:`ServerDefinition`: Server definition with the specified
          nickname.

        Raises:
          KeyError: Nickname not found
        """
        try:
            server_dict = self._servers[nickname]
        except KeyError:
            new_exc = KeyError(
                "Server with nickname {!r} not found in server definition "
                "file {!r}".
                format(nickname, self._filepath))
            new_exc.__cause__ = None
            raise new_exc  # KeyError
        return ServerDefinition(nickname, server_dict)

    def list_servers(self, nickname):
        """
        List the server definitions for a given server or server group nickname.

        Parameters:
          nickname (string): Server or server group nickname.

        Returns:
          list of class:`ServerDefinition`: List of server definitions.

        Raises:
          KeyError: Nickname not found
        """
        if nickname in self._servers:
            return [self.get_server(nickname)]

        if nickname in self._server_groups:
            sd_list = list()  # of ServerDefinition objects
            sd_nick_list = list()  # of server nicknames
            sg_item = self._server_groups[nickname]
            for member_nick in sg_item['members']:
                member_sds = self.list_servers(member_nick)
                for sd in member_sds:
                    if sd.nickname not in sd_nick_list:
                        sd_nick_list.append(sd.nickname)
                        sd_list.append(sd)
            return sd_list

        raise KeyError(
            "Server or server group with nickname {!r} not found in server "
            "definition file {!r}".
            format(nickname, self._filepath))

    def list_default_servers(self):
        """
        List the server definitions for the default server or group.

        An omitted 'default' element in the server definition file results in
        an empty list.

        Returns:
          list of class:`ServerDefinition`: List of server definitions.
        """
        if self._default is None:
            return []
        return self.list_servers(self._default)

    def list_all_servers(self):
        """
        List all server definitions.

        Returns:
          list of class:`ServerDefinition`: List of server definitions.
        """
        return [self.get_server(nickname) for nickname in self._servers]


def _load_validate_default(filepath):
    """
    Load the server definition file, validate its format and default some
    optional elements.

    Returns:
      dict: Python dict representing the file content.

    Raises:
      ServerDefinitionFileNotFound: File not found, incl. permission errors
      ServerDefinitionFileError: Invalid file content
      RuntimeError: Internal errors
    """

    # Load the server definition file (YAML)
    try:
        with open(filepath, 'r') as fp:
            data = yaml.safe_load(fp)
    except (OSError, IOError) as exc:
        new_exc = ServerDefinitionFileNotFound(
            "Cannot open server definition file: {fn}: {exc}".
            format(fn=filepath, exc=exc))
        new_exc.__cause__ = None  # pylint: disable=invalid-name
        raise new_exc  # ServerDefinitionFileNotFound
    except yaml.YAMLError as exc:
        new_exc = ServerDefinitionFileError(
            "Invalid YAML syntax in server definition file {fn}: {exc}".
            format(fn=filepath, exc=exc))
        new_exc.__cause__ = None  # pylint: disable=invalid-name
        raise new_exc  # ServerDefinitionFileError

    # Schema validation of file content
    try:
        jsonschema.validate(data, SERVER_DEFINITION_FILE_SCHEMA)
        # Raises jsonschema.exceptions.SchemaError if JSON schema is invalid
    except jsonschema.exceptions.ValidationError as exc:
        if exc.absolute_path:
            elem_str = "element '{}'". \
                format('.'.join(str(e) for e in exc.absolute_path))
        else:
            elem_str = 'top-level element'

        new_exc = ServerDefinitionFileError(
            "Invalid format in server definition file {fn}: Validation "
            "failed on {elem}: {exc}".
            format(fn=filepath, elem=elem_str, exc=exc))
        new_exc.__cause__ = None
        raise new_exc  # ServerDefinitionFileError

    # Establish defaults for optional top-level elements

    if 'server_groups' not in data:
        data['server_groups'] = {}

    if 'default' not in data:
        data['default'] = None

    # Additional semantic validation

    # TODO: Check that default exists
    # TODO: Check that server group members exist

    return data
