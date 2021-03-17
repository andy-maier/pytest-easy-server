"""
Test import and versioning of the package.
"""

from __future__ import absolute_import, print_function


def test_import():
    """
    Test import of the package.
    """
    # pylint: disable=import-outside-toplevel
    import client_end2end_tester  # noqa: F401
    assert client_end2end_tester


def test_versioning():
    """
    Test import of the package.
    """
    # pylint: disable=import-outside-toplevel
    import client_end2end_tester  # noqa: F401
    assert client_end2end_tester.__version__
