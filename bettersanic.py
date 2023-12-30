from sanic import Sanic
import importlib
from typing import Iterable, Optional, Union, List, Any, Literal, Protocol, Callable


class BetterSanicData:
    pass


class RouteData(BetterSanicData):
    def __init__(
        self,
        uri: str,
        methods: Iterable[str] = frozenset({"GET"}),
        host: Optional[Union[str, List[str]]] = None,
        strict_slashes: Optional[bool] = None,
        version: Optional[Union[int, str, float]] = None,
        name: Optional[str] = None,
        stream: bool = False,
        version_prefix: str = "/v",
        error_format: Optional[str] = None,
        **ctx_kwargs: Any,
    ):
        self.uri = uri
        self.methods = methods
        self.host = host
        self.strict_slashes = strict_slashes
        self.version = version
        self.name = name
        self.stream = stream
        self.version_prefix = version_prefix
        self.error_format = error_format
        self.ctx_kwargs = ctx_kwargs


class ExceptionData(BetterSanicData):
    def __init__(self, exceptions: tuple[type[BaseException], ...], apply: bool = True):
        self.exceptions = exceptions
        self.apply = apply


class ListenerData(BetterSanicData):
    def __init__(self, event: str):
        self.event = event


class MiddlewareData(BetterSanicData):
    def __init__(
        self,
        attach_to: Union[Literal["request"], Literal["response"]],
        apply: bool = True,
        *,
        priority: int = 0,
    ):
        self.attach_to = attach_to
        self.apply = apply
        self.priority = priority


class WebsocketData(BetterSanicData):
    def __init__(
        self,
        uri: str,
        host: Optional[Union[str, List[str]]] = None,
        strict_slashes: Optional[bool] = None,
        subprotocols: Optional[List[str]] = None,
        version: Optional[Union[int, str, float]] = None,
        name: Optional[str] = None,
        apply: bool = True,
        version_prefix: str = "/v",
        error_format: Optional[str] = None,
        **ctx_kwargs: Any,
    ):
        self.uri = uri
        self.host = host
        self.strict_slashes = strict_slashes
        self.subprotocols = subprotocols
        self.version = version
        self.name = name
        self.apply = apply
        self.version_prefix = version_prefix
        self.error_format = error_format
        self.ctx_kwargs = ctx_kwargs


class MethodWithRouteData(Protocol):
    bettersanic_data: RouteData


class MethodWithExceptionData(Protocol):
    bettersanic_data: ExceptionData


class MethodWithMiddlewareData(Protocol):
    bettersanic_data: MiddlewareData


class MethodWithListenerData(Protocol):
    bettersanic_data: ListenerData


class MethodWithWebsocketData(Protocol):
    bettersanic_data: WebsocketData


class Cog:
    routes: List[MethodWithRouteData]
    exceptions: List[MethodWithExceptionData]
    middlewares: List[MethodWithMiddlewareData]
    listeners: List[MethodWithListenerData]
    websockets: List[MethodWithWebsocketData]

    def __new__(cls, *args: Any, **kwargs: Any):
        new_cls = super().__new__(cls)
        bettersanic_funcs = [
            getattr(new_cls, name)
            for name, func in cls.__dict__.items()
            if callable(func)
            and hasattr(func, "bettersanic_data")
            and isinstance(func.bettersanic_data, BetterSanicData)
        ]
        new_cls.routes = [
            func
            for func in bettersanic_funcs
            if isinstance(func.bettersanic_data, RouteData)
        ]
        new_cls.exceptions = [
            func
            for func in bettersanic_funcs
            if isinstance(func.bettersanic_data, ExceptionData)
        ]
        new_cls.middlewares = [
            func
            for func in bettersanic_funcs
            if isinstance(func.bettersanic_data, MiddlewareData)
        ]
        new_cls.listeners = [
            func
            for func in bettersanic_funcs
            if isinstance(func.bettersanic_data, ListenerData)
        ]
        new_cls.websockets = [
            func
            for func in bettersanic_funcs
            if isinstance(func.bettersanic_data, WebsocketData)
        ]

        return new_cls


class BetterSanic(Sanic):
    def add_cog(self, cog: Cog):
        for route_handler in cog.routes:
            data = route_handler.bettersanic_data
            self.add_route(
                route_handler,  # type: ignore # not my fault
                data.uri,
                data.methods,
                data.host,
                data.strict_slashes,
                data.version,
                data.name,
                data.stream,
                data.version_prefix,
                data.error_format,
                **data.ctx_kwargs,
            )
        for exception_handler in cog.exceptions:
            data = exception_handler.bettersanic_data
            for exception in data.exceptions:
                self.error_handler.add(exception, exception_handler)  # type: ignore # not my fault
        for listener_handler in cog.listeners:
            data = listener_handler.bettersanic_data
            self.register_listener(listener_handler, data.event)  # type: ignore # not my fault
        for middleware_handler in cog.middlewares:
            data = middleware_handler.bettersanic_data
            self.register_middleware(
                middleware_handler, data.attach_to  # type: ignore # not my fault
            )
        for websocket_handler in cog.websockets:
            data = websocket_handler.bettersanic_data
            self.add_websocket_route(  # type: ignore # not my fault
                websocket_handler,
                data.uri,
                data.host,
                data.strict_slashes,
                data.subprotocols,
                data.version,
                data.name,
                data.version_prefix,
                data.error_format,
                **data.ctx_kwargs,
            )

    def load_extension(self, name: str):
        return importlib.import_module(name).setup(self)


def route(
    uri: str,
    methods: Iterable[str] = frozenset({"GET"}),
    host: Optional[Union[str, List[str]]] = None,
    strict_slashes: Optional[bool] = None,
    version: Optional[Union[int, str, float]] = None,
    name: Optional[str] = None,
    stream: bool = False,
    version_prefix: str = "/v",
    error_format: Optional[str] = None,
    **ctx_kwargs: Any,
):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.bettersanic_data = RouteData(  # type: ignore # dont know how to fix
            uri,
            methods,
            host,
            strict_slashes,
            version,
            name,
            stream,
            version_prefix,
            error_format,
            **ctx_kwargs,
        )
        return func

    return decorator


def exception(*exceptions: type[BaseException], apply: bool = True):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.bettersanic_data = ExceptionData(exceptions, apply)  # type: ignore # dont know how to fix
        return func

    return decorator


def listener(event: str):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.bettersanic_data = ListenerData(event)  # type: ignore # dont know how to fix
        return func

    return decorator


def middleware(
    attach_to: Union[Literal["request"], Literal["response"]],
    apply: bool = True,
    *,
    priority: int = 0,
):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.bettersanic_data = MiddlewareData(attach_to, apply, priority=priority)  # type: ignore # dont know how to fix
        return func

    return decorator


def websocket(
    uri: str,
    host: Optional[Union[str, List[str]]] = None,
    strict_slashes: Optional[bool] = None,
    subprotocols: Optional[List[str]] = None,
    version: Optional[Union[int, str, float]] = None,
    name: Optional[str] = None,
    apply: bool = True,
    version_prefix: str = "/v",
    error_format: Optional[str] = None,
    **ctx_kwargs: Any,
):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        func.bettersanic_data = WebsocketData(  # type: ignore # dont know how to fix
            uri,
            host,
            strict_slashes,
            subprotocols,
            version,
            name,
            apply,
            version_prefix,
            error_format,
            **ctx_kwargs,
        )
        return func

    return decorator
