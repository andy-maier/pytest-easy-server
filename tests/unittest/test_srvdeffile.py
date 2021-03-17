"""
Test the _srvdef.py module.
"""

from __future__ import absolute_import, print_function
import os
import pytest
from testfixtures import TempDirectory
import six
from client_end2end_tester import ServerDefinitionFile, \
    ServerDefinitionFileError

from ..utils.simplified_test_function import simplified_test_function


TESTCASES_SERVER_DEFINITION_FILE_INIT = [

    # Testcases for ServerDefinitionFile.__init__()

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * init_args: Tuple of positional arguments to ServerDefinitionFile().
    #   * init_kwargs: Dict of keyword arguments to ServerDefinitionFile().
    #   * exp_attrs: Dict with expected ServerDefinitionFile attributes.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Basic parameter checking
    (
        "Order of positional parameters",
        dict(
            init_args=(
                'myfile',
            ),
            init_kwargs=dict(),
            exp_attrs={
                'filepath': 'myfile',
            },
        ),
        None, None, True
    ),
    (
        "Names of keyword arguments",
        dict(
            init_args=(),
            init_kwargs=dict(
                filepath='myfile',
            ),
            exp_attrs={
                'filepath': 'myfile',
            },
        ),
        None, None, True
    ),

    # Omitted init parameters
    (
        "Omitted optional parameter: filepath",
        dict(
            init_args=(),
            init_kwargs=dict(),
            exp_attrs={
                'filepath': ServerDefinitionFile.default_filepath,
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SERVER_DEFINITION_FILE_INIT)
@simplified_test_function
def test_ServerDefinitionFile_init(testcase, init_args, init_kwargs, exp_attrs):
    """
    Test function for ServerDefinitionFile.__init__()
    """

    # The code to be tested
    act_obj = ServerDefinitionFile(*init_args, **init_kwargs)

    # Ensure that exceptions raised in the remainder of this function
    # are not mistaken as expected exceptions
    assert testcase.exp_exc_types is None

    for attr_name in exp_attrs:
        exp_attr_value = exp_attrs[attr_name]
        assert hasattr(act_obj, attr_name), \
            "Missing attribute {0!r} in returned ServerDefinitionFile object". \
            format(attr_name)
        act_attr_value = getattr(act_obj, attr_name)
        assert act_attr_value == exp_attr_value, \
            "Unexpected value for attribute {0!r}: Expected {1!r}, got {2!r}".\
            format(attr_name, exp_attr_value, act_attr_value)


TESTCASES_SERVER_DEFINITION_FILE_DATA = [

    # Testcases for ServerDefinitionFile.data (load&verify)

    # Each list item is a testcase tuple with these items:
    # * desc: Short testcase description.
    # * kwargs: Keyword arguments for the test function:
    #   * sdf_yaml: Content of server definition file.
    #   * exp_data: Expected ServerDefinitionFile.data attribute.
    # * exp_exc_types: Expected exception type(s), or None.
    # * exp_warn_types: Expected warning type(s), or None.
    # * condition: Boolean condition for testcase to run, or 'pdb' for debugger

    # Basic validation
    (
        "Empty file: Missing required 'servers' element",
        dict(
            sdf_yaml="",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid YAML syntax: Mixing list and dict",
        dict(
            sdf_yaml="servers:\n"
                     "  - foo\n"
                     "  bar:\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid top-level type list",
        dict(
            sdf_yaml="- servers: {}\n"
                     "- server_groups: {}\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Missing required 'servers' element",
        dict(
            sdf_yaml="server_groups: {}\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for 'servers' element: list",
        dict(
            sdf_yaml="servers:\n"
                     "  - foo\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for 'servers' element: string",
        dict(
            sdf_yaml="servers: bla\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for 'server_groups' element: list",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups: []\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for 'server_groups' element: string",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups: bla\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for server group: dict",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    srv1: {}\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for server group: string",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1: srv1\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for server group member: dict",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    - srv1: {}\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),
    (
        "Invalid type for server group member: list",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    - srv1: []\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),

    # More semantic errors
    (
        "Server group member not defined in servers",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups:\n"
                     "  grp1:\n"
                     "    - srv1\n",
            exp_data=None,
        ),
        ServerDefinitionFileError, None, True
    ),

    # Valid simple server definition files
    (
        "Valid file with no servers and omitted 'server_groups' item",
        dict(
            sdf_yaml="servers: {}\n",
            exp_data={
                'servers': {},
            },
        ),
        None, None, True
    ),
    (
        "Valid file with no servers and no server groups",
        dict(
            sdf_yaml="servers: {}\n"
                     "server_groups: {}\n",
            exp_data={
                'servers': {},
                'server_groups': {},
            },
        ),
        None, None, True
    ),
    (
        "Valid file with one server",
        dict(
            sdf_yaml="servers:\n"
                     "  srv1:\n"
                     "    description: server1\n"
                     "    details:\n"
                     "      stuff: 42\n",
            exp_data={
                'servers': {
                    'srv1': {
                        'description': 'server1',
                        'details': {
                            'stuff': 42,
                        },
                    },
                },
            },
        ),
        None, None, True
    ),
]


@pytest.mark.parametrize(
    "desc, kwargs, exp_exc_types, exp_warn_types, condition",
    TESTCASES_SERVER_DEFINITION_FILE_DATA)
@simplified_test_function
def test_ServerDefinitionFile_data(testcase, sdf_yaml, exp_data):
    """
    Test function for ServerDefinitionFile.data
    """

    with TempDirectory() as tmp_dir:

        # Create the server definition file
        filename = 'tmp_sdf.yaml'
        filepath = os.path.join(tmp_dir.path, filename)
        if isinstance(sdf_yaml, six.text_type):
            sdf_yaml = sdf_yaml.encode('utf-8')
        tmp_dir.write(filename, sdf_yaml)

        sdf = ServerDefinitionFile(filepath)

        # The code to be tested
        act_data = sdf.data

        # Ensure that exceptions raised in the remainder of this function
        # are not mistaken as expected exceptions
        assert testcase.exp_exc_types is None

        assert act_data == exp_data
