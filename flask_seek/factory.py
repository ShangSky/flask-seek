from typing import Callable, Any, Optional
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


class FunctionFactory:
    def __getattr__(self, item: str) -> Callable:
        def decorator(*args: Any, **kwargs: Any) -> Callable:
            return wrapper("errorhandler", args, kwargs)

        return decorator


df = DecoratorFactory()
ff = FunctionFactory()
