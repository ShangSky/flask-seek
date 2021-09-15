import pkgutil
from typing import Callable, Iterable, Optional, Type, TypeVar, Any
from types import ModuleType
from importlib import import_module

T = TypeVar("T")


def find_modules(
    pkg_name: str, *, deep: bool = False, lazy: bool = False
) -> Iterable[ModuleType]:
    pkg = import_module(pkg_name)
    module_path = getattr(pkg, "__path__", None)
    if module_path is None:
        return [pkg]
    iter_modules_func = pkgutil.walk_packages if deep else pkgutil.iter_modules
    iter_modules = (
        import_module(module_info[1])
        for module_info in iter_modules_func(module_path, pkg.__name__ + ".")
        if not module_info[2]
    )
    return iter_modules if lazy else list(iter_modules)


def get_objs(
    module: ModuleType, cls: Type[T], func: Optional[Callable[[Any, Any], bool]] = None
) -> Iterable[T]:
    for attr_name in dir(module):
        if not attr_name.startswith("__"):
            attr = getattr(module, attr_name)
            call = func or isinstance
            if call(attr, cls):
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
    pkg_names: Iterable[str],
    cls: Type[T],
    *,
    deep: bool = False,
    func: Optional[Callable[[Any, Any], bool]] = None
) -> Iterable[T]:
    obj_ids = set()
    for pkg_name in pkg_names:
        modules = find_modules(pkg_name, deep=deep)
        for module in modules:
            for obj in get_objs(module, cls, func=func):
                obj_id = id(obj)
                if obj_id not in obj_ids:
                    obj_ids.add(obj_id)
                    yield obj
