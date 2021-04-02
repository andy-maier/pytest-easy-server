"""
Example pytest test function for pytest-easy-server project.
"""

# pylint: disable=unused-import
from pytest_easy_server import es_server  # noqa: F401


class MySession(object):
    """Fictitious session class with dummy methods"""

    def __init__(self, host, username, password):
        """Open session with the server"""
        print("\nMySession: host={}, username={}, password={}".
              format(host, username, password))

    @staticmethod
    def perform_function():
        """Perform some function on the server"""
        return 42

    @staticmethod
    def close():
        """Close session with the server"""
        pass


def test_sample(es_server):  # pylint: disable=redefined-outer-name
    """
    Example Pytest test function that tests something.

    Parameters:
      es_server (easy_server.Server): Pytest fixture; the server to be
        used for the test
    """

    # Standard properties from the server file:
    # nickname = es_server.nickname
    # description = es_server.description

    # User-defined additional properties from the server file:
    # stuff = es_server.user_defined['stuff']

    # User-defined secrets from the vault file:
    host = es_server.secrets['host']
    username = es_server.secrets['username']
    password = es_server.secrets['password']

    # Session to server using a fictitious session class
    session = MySession(host, username, password)

    # Test something
    result = session.perform_function()
    assert result == 42

    # Cleanup
    session.close()
