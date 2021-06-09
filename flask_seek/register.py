from typing import Iterable, Union, Optional

from flask import Flask, Blueprint

from flask_seek.util import get_objs_in_modules
from flask_seek.factory import MethodProxy


def register_blueprints(
    instance: Union[Flask, Blueprint], pkg_names: Iterable[str], *, deep: bool = False
) -> None:
    for obj in get_objs_in_modules(pkg_names, Blueprint, deep=deep):
        instance.register_blueprint(obj)


def register_methods(
    instance: Union[Flask, Blueprint], pkg_names: Iterable[str], *, deep: bool = False
) -> None:
    for obj in get_objs_in_modules(pkg_names, MethodProxy, deep=deep):
        method = getattr(instance, obj.method_name, None)
        if method is not None:
            if obj.args is None:
                method(obj.f)
            else:
                method(*obj.args, **obj.kwargs)(obj.f)


def seek(
    instance: Union[Flask, Blueprint],
    *,
    blueprint_modules: Optional[Iterable[str]] = None,
    blueprint_deep_modules: Optional[Iterable[str]] = None,
    method_modules: Optional[Iterable[str]] = None,
    method_deep_modules: Optional[Iterable[str]] = None
) -> None:
    if blueprint_modules:
        register_blueprints(instance, blueprint_modules)
    if blueprint_deep_modules:
        register_blueprints(instance, blueprint_deep_modules, deep=True)
    if method_modules:
        register_methods(instance, method_modules)
    if method_deep_modules:
        register_methods(instance, method_deep_modules, deep=True)
