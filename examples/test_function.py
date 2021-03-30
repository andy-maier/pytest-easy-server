"""
Example pytest test function for pytest-easy-server project.
"""

from pytest_easy_server import es_server

def test_sample(es_server):
    """
    Example Pytest test function that tests something.

    Parameters:
      es_server (easy_server.Server): Server to be used.
    """

    # Standard properties from the server file:
    nickname = es_server.nickname
    description = es_server.description

    # User-defined additional properties from the server file:
    stuff = es_server.user_defined['stuff']

    # User-defined secrets from the vault file:
    host = es_server.secrets['host']
    username = es_server.secrets['username']
    password = es_server.secrets['password']

    # Log on to the host and perform some test
    # . . .
