"""
Example pytest test function for pytest-easy-server project.
"""

from pytest_easy_server import server_definition

def test_sample(server_definition):
    """
    Example Pytest test function that tests something.

    Parameters:
      server_definition (easy_server.ServerDefinition): Server to be used.
    """

    # Standard properties from the server definition file:
    nickname = server_definition.nickname
    description = server_definition.description

    # User-defined additional properties from the server definition file:
    stuff = server_definition.user_defined['stuff']

    # User-defined secrets from the vault file:
    host = server_definition.secrets['host']
    username = server_definition.secrets['username']
    password = server_definition.secrets['password']

    # Log on to the host and perform some test
    # . . .
