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
          NICKNAME1:            # Nickname of the server.
            description: TEXT   # Short description of the server.
            contact_name: TEXT  # Name of technical contact for the server.
            access_via: TEXT    # Short reminder on the network/firewall/proxy/
                                # vpn used to access the server.
            details:            # Details of the server, such as IP address.

        server_groups:          # Server groups.
          NICKNAME42:           # Nickname of server group.
            - NICKNAME1         # Nicknames of members (servers or groups).
            - NICKNAME2
    """

    default_filepath = 'examples/server_definitions.yaml'

    def __init__(self, filepath=None):
        if filepath is None:
            filepath = self.default_filepath
        self._filepath = filepath
        self._data = None
        self._servers = None
        self._server_groups = None

    @property
    def filepath(self):
        """
        string: File path of the server definition file.
        """
        return self._filepath

    @property
    def data(self):
        """
        dict: Data in the server definition file, parsed and validated.
        """
        if self._data is None:
            self._data = load_and_validate(self._filepath)
        return self._data

    @property
    def servers(self):
        """
        list: Servers in the server definition file.
        """
        if self._servers is None:
            self._servers = self.data['servers']
        return self._servers

    @property
    def server_groups(self):
        """
        list: Server groups in the server definition file, or empty list if
        none is defined.
        """
        if self._server_groups is None:
            try:
                self._server_groups = self.data['server_groups']
            except KeyError:
                self.data['server_groups'] = []
                self._server_groups = self.data['server_groups']
        return self._server_groups

    def get_server(self, nickname):
        """
        Return a `ServerDefinition` object for the server with the specified
        server nickname.

        Raises:
          KeyError: Server not found
        """
        try:
            server_dict = self.servers[nickname]
        except KeyError:
            raise KeyError(
                "Server with nickname {!r} not found in server definition "
                "file {!r}".
                format(nickname, self._filepath))
        return ServerDefinition(nickname, server_dict)

    def list_servers(self, nickname):
        """
        Return a list of `ServerDefinition` objects that contains the servers
        in the server group with the specified group nickname, or the single
        server with the specified server nickname.

        Raises:
          KeyError: Server or server group not found
        """
        if nickname in self.servers:
            return [self.get_server(nickname)]

        if nickname in self.server_groups:
            sd_list = list()  # of ServerDefinition objects
            sd_nick_list = list()  # of server nicknames
            for server_nick in self.server_groups[nickname]:
                for sd in self.list_servers(server_nick):
                    if sd.nickname not in sd_nick_list:
                        sd_list.append(sd)
                        sd_nick_list.append(sd.nickname)
            return sd_list

        raise KeyError(
            "Server group or server with nickname {!r} not found in "
            "server definition file {!r}".
            format(nickname, self._filepath))

    def list_all_servers(self):
        """
        Return a list of `ServerDefinition` objects for all servers in the
        server definition file.
        """
        return [self.get_server(nickname) for nickname in self.servers]


def load_and_validate(filepath):
    """
    Load the server definition file and validate its format.

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
            "Invalid YAML in server definition file {fn}: {exc}".
            format(fn=filepath, exc=exc))
        new_exc.__cause__ = None  # pylint: disable=invalid-name
        raise new_exc  # ServerDefinitionFileError

    # Schema validation of file content
    try:
        jsonschema.validate(data, SERVER_DEFINITION_FILE_SCHEMA)
    except jsonschema.exceptions.SchemaError as exc:
        new_exc = ValueError(
            "Invalid server definition file JSON schema (internal error): "
            "{exc}".
            format(exc=exc))
        new_exc.__cause__ = None
        raise new_exc  # RuntimeError
    except jsonschema.exceptions.ValidationError as exc:
        if exc.absolute_path:
            elem_str = "element '{}'". \
                format('.'.join(str(e) for e in exc.absolute_path))
        else:
            elem_str = 'top-level element'

        new_exc = ServerDefinitionFileError(
            "Invalid format of server definition file {fn}: Validation "
            "failed on {elem}: {exc}".
            format(fn=filepath, elem=elem_str, exc=exc))
        new_exc.__cause__ = None
        raise new_exc  # ServerDefinitionFileError

    return data
