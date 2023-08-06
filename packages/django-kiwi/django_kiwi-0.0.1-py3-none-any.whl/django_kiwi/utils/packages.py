import inspect
import pkgutil
import sys
from typing import Callable


def list_submodules(list_name: list, package_name: str) -> None:
    '''
        Append all submodules on list_name from package

        Parameters:
            list_name (list): List of submodules names
            package_name (str): Root package name, for subpackages use dot

        Returns:
            List of python modules inside a package

    '''

    for _, module_name, is_pkg in pkgutil.walk_packages(
            package_name.__path__, f'{package_name.__name__}.'):
        list_name.append(module_name)
        module_name = __import__(module_name, fromlist='dummylist')
        if is_pkg:
            list_submodules(list_name, module_name)


def get_all_modules(package_name: str) -> list:
    '''
        Get all modules from package

        Parameters:
            package_name (str): Root package name, for subpackages use dot
                Ex: tickets.actions

        Returns:
            List of python modules inside a package

    '''
    package = __import__(package_name, fromlist='dummylist')
    all_modules = []
    list_submodules(all_modules, package)
    return all_modules


def get_classes_from_package(package_name: str, filter_method: Callable = lambda x: x):
    '''
        Get classes from package

        Parameters:
            package_name (str): Root package name, for subpackages use dot
            filter_method (Callable): Filter class method, receive instance of class

        Returns:
            List of classes inside a package

    '''

    filtered_classes = []

    for module in list(set(get_all_modules(package_name))):
        classes = inspect.getmembers(sys.modules[module], inspect.isclass)
        for _, instance in classes:
            if filter_method(instance):
                filtered_classes.append(instance)
    return filtered_classes


def get_class_from_package(package_name: str, filter_method: Callable):
    '''
        Get classes from package

        Parameters:
            package_name (str): Root package name, for subpackages use dot
            filter_method (Callable): Filter class method, receive instance of class

        Returns:
            Intance of class inside a package or None if not found

    '''

    classes = get_classes_from_package(package_name, filter_method)

    if len(classes) == 1:
        return classes[0]

    if not classes:
        return None

    raise ValueError('Return more than one class')
