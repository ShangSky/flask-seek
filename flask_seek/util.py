import pkgutil
from typing import Iterable, Type, TypeVar, Any
from types import ModuleType
from importlib import import_module

T = TypeVar("T")


def find_modules(pkg_name: str, *, deep: bool = False) -> Iterable[ModuleType]:
    pkg = import_module(pkg_name)
    module_path = getattr(pkg, "__path__", None)
    if module_path is None:
        return [pkg]
    iter_modules = pkgutil.walk_packages if deep else pkgutil.iter_modules
    return (
        import_module(module_info[1])
        for module_info in iter_modules(module_path, pkg.__name__ + ".")
        if not module_info[2]
    )


def get_objs(module: ModuleType, cls: Type[T]) -> Iterable[T]:
    for attr_name in dir(module):
        if not attr_name.startswith("__"):
            attr = getattr(module, attr_name)
            if isinstance(attr, cls):
                yield attr


def import_string(dotted_path: str) -> Any:
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "{}" does not define a "{}" attribute/class'.format(
                module_path, class_name
            )
        ) from err


def get_objs_in_modules(
    pkg_names: Iterable[str], cls: Type[T], *, deep: bool = False
) -> Iterable[T]:
    obj_ids = set()
    for pkg_name in pkg_names:
        modules = list(find_modules(pkg_name, deep=deep))
        for module in modules:
            for obj in get_objs(module, cls):
                obj_id = id(obj)
                if obj_id not in obj_ids:
                    obj_ids.add(obj_id)
                    yield obj
