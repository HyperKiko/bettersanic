from sanic import Sanic
import importlib

class BetterSanicData: pass

class RouteData(BetterSanicData):
    def __init__(self, location, *args, **kwargs):
        self.type = "route"
        self.location = location
        self.args = args
        self.kwargs = kwargs


class ExceptionData(BetterSanicData):
    def __init__(self, *exceptions, **kwargs):
        self.type = "exception"
        self.exceptions = exceptions
        self.kwargs = kwargs

class ListenerData(BetterSanicData):
    def __init__(self, event, *args, **kwargs):
        self.type = "listener"
        self.event = event
        self.args = args
        self.kwargs = kwargs

class MiddlewareData(BetterSanicData):
    def __init__(self, attach_to, *args, **kwargs):
        self.type = "middleware"
        self.attach_to = attach_to
        self.args = args
        self.kwargs = kwargs

class WebsocketData(BetterSanicData):
    def __init__(self, location, *args, **kwargs):
        self.type = "websocket"
        self.location = location
        self.args = args
        self.kwargs = kwargs

class Cog:
    def __new__(cls, *args, **kwargs):
        new_cls = super().__new__(cls)
        bettersanic_funcs = [getattr(new_cls, name) for name, func in cls.__dict__.items(
        ) if hasattr(func, "_bettersanic_data") and isinstance(func._bettersanic_data, BetterSanicData)]
        new_cls.routes = [
            route for route in bettersanic_funcs if route._bettersanic_data.type == "route"]
        new_cls.exceptions = [
            exception for exception in bettersanic_funcs if exception._bettersanic_data.type == "exception"]
        new_cls.listeners = [
            listener for listener in bettersanic_funcs if listener._bettersanic_data.type == "listener"]
        new_cls.middlewares = [
            middleware for middleware in bettersanic_funcs if middleware._bettersanic_data.type == "middleware"]
        new_cls.websockets = [
            websocket for websocket in bettersanic_funcs if websocket._bettersanic_data.type == "websocket"]

        return new_cls


class BetterSanic(Sanic):
    def add_cog(self, cog):
        for websocket in cog.routes:
            data = websocket._bettersanic_data
            self.add_route(websocket, data.location, *data.args, **data.kwargs)
        for exception in cog.exceptions:
            data = exception._bettersanic_data
            for exception_type in data.exceptions:
                self.error_handler.add(
                    exception_type, exception, **data.kwargs)
        for middleware in cog.listeners:
            data = middleware._bettersanic_data
            self.register_listener(middleware, data.event, *data.args, *data.kwargs)
        for middleware in cog.middlewares:
            data = middleware._bettersanic_data
            self.register_middleware(middleware, data.attach_to, *data.args, *data.kwargs)
        for websocket in cog.websockets:
            data = websocket._bettersanic_data
            self.add_websocket_route(websocket, data.location, *data.args, **data.kwargs)

    def load_extension(self, name):
        return importlib.import_module(name).setup(self)


def route(location, *args, **kwargs):
    def decorator(func):
        func._bettersanic_data = RouteData(location, *args, **kwargs)
        return func
    return decorator


def exception(*exceptions, **kwargs):
    def decorator(func):
        func._bettersanic_data = ExceptionData(*exceptions, **kwargs)
        return func
    return decorator

def listener(event, *args, **kwargs):
    def decorator(func):
        func._bettersanic_data = ListenerData(event, *args, **kwargs)
        return func
    return decorator

def middleware(attach_to, *args, **kwargs):
    def decorator(func):
        func._bettersanic_data = MiddlewareData(attach_to, *args, **kwargs)
        return func
    return decorator

def websocket(location, *args, **kwargs):
    def decorator(func):
        func._bettersanic_data = WebsocketData(location, *args, **kwargs)
        return func
    return decorator