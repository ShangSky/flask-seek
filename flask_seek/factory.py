from typing import Callable, Any, Optional, Union, Type, TYPE_CHECKING
from functools import update_wrapper


class MethodProxy:
    def __init__(
        self,
        f: Callable,
        method_name: str,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
    ) -> None:
        self.f = f
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        update_wrapper(self, f)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.f(*args, **kwargs)


def wrapper(
    method_name: str, args: Optional[tuple] = None, kwargs: Optional[dict] = None
) -> Callable[[Callable], MethodProxy]:
    def inner(f: Callable) -> MethodProxy:
        return MethodProxy(f=f, method_name=method_name, args=args, kwargs=kwargs)

    return inner


class DecoratorFactory:
    def __getattr__(self, item: str) -> Callable[[Callable], MethodProxy]:
        def decorator(f: Callable) -> MethodProxy:
            return MethodProxy(f=f, method_name=item)

        return decorator

    if TYPE_CHECKING:
        def before_first_request(self, f: Callable) -> Callable: ...
        def teardown_appcontext(self, f: Callable) -> Callable: ...
        def shell_context_processor(self, f: Callable) -> Callable: ...
        def before_request(self, f: Callable) -> Callable: ...
        def after_request(self, f: Callable) -> Callable: ...
        def teardown_request(self, f: Callable) -> Callable: ...
        def context_processor(self, f: Callable) -> Callable: ...
        def url_value_preprocessor(self, f: Callable) -> Callable: ...
        def url_defaults(self, f: Callable) -> Callable: ...


class FunctionFactory:
    def __getattr__(self, item: str) -> Callable:
        def decorator(*args: Any, **kwargs: Any) -> Callable:
            return wrapper(item, args, kwargs)

        return decorator

    if TYPE_CHECKING:
        def template_filter(self, name: Optional[str] = None) -> Callable[[
            Callable], Callable]: ...

        def template_test(self, name: Optional[str] = None) -> Callable[[
            Callable], Callable]: ...

        def template_global(self, name: Optional[str] = None) -> Callable[[
            Callable], Callable]: ...

        def errorhandler(self, code_or_exception: Union[Type[Exception], int]) -> Callable[[
            Callable], Callable]: ...


df = DecoratorFactory()
ff = FunctionFactory()
