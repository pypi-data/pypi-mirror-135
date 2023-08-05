try:
    import importlib.resources as resources
except ImportError:  # pragma: no cover
    import importlib_resources as resources

from logging import debug
from robotlibcore import DynamicCore, keyword
from robot.libraries.BuiltIn import BuiltIn
from typing import Iterable

from ._version import __version__


def load_resource_file(
    package: resources.Package,
    resources_: Iterable[resources.Resource]
):
    built_in = BuiltIn()

    for resource in resources_:
        with resources.path(package, resource) as path:
            debug(f'Importing resource file from {path}')
            built_in.import_resource(str(path))


def _parse_args_and_load_resource_file(args):
    if len(args) < 2:
        raise ValueError(
            'Not enough arguments. Expected package name as first argument and resource names as following arguments.')
    load_resource_file(args[0], args[1:])


class SharedResources(DynamicCore):
    '''Library for importing Robot Framework resource files from python libraries.

    To include non-python files, in this case ``.robot`` or ``.resource`` files, to the Python package, use ``package_data`` or ``include_package_data`` settings of Python setuptools to configure files to be included in the package. See setuptools [https://setuptools.pypa.io/en/latest/userguide/datafiles.html#data-files-support|documentation] for details.
    '''

    ROBOT_LISTENER_API_VERSION = 2
    __version__ = __version__

    def __init__(self, *args):
        '''
        Can be either imported without parameters or with parameters of `Import resource from package`. If parameters are given, the resources defined by the parameters are imported during the library initialization.

        Examples:
        | Library | SharedResources |
        | Library | SharedResources | EmbeddedResources.resources | a_keywords.resource | b_keywords.robot |
        '''
        self.ROBOT_LIBRARY_LISTENER = self  # pylint: disable=invalid-name
        '''Due to RF library import caching the `__init__()` method is called only once per unique args list. Thus listener API has to be used to do resource file loading when library is imported again with same arguments. See `library_import()` method.'''
        DynamicCore.__init__(self, [])
        if args:
            _parse_args_and_load_resource_file(args)

    @keyword
    def import_resource_from_package(
            self,
            package: resources.Package,
            *resources_: resources.Resource):
        '''Imports a resource file embedded in Python packages resources.

        Examples:
        | Import resource from package | EmbeddedResources.resources | a_keywords.resource |
        | Import resource from package | EmbeddedResources.resources | a_keywords.resource | b_keywords.robot |
        '''
        load_resource_file(package, resources_)

    def library_import(self, _, attributes):
        '''Listener for library import notifications

        Listen for library import notifications and load resource files when this library is imported. See also `ROBOT_LIBRARY_LISTENER` instance variable in `__init__()` method.
        '''
        name = attributes.get('originalname')
        args = attributes.get('args')

        if name == self.__class__.__name__:
            _parse_args_and_load_resource_file(args)
