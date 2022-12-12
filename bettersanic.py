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


class Cog:
    def __new__(cls, *args, **kwargs):
        new_cls = super().__new__(cls)
        bettersanic_funcs = [getattr(new_cls, name) for name, func in cls.__dict__.items(
        ) if hasattr(func, "_bettersanic_data") and isinstance(func._bettersanic_data, BetterSanicData)]
        new_cls.routes = [
            route for route in bettersanic_funcs if route._bettersanic_data.type == "route"]
        new_cls.exceptions = [
            exception for exception in bettersanic_funcs if exception._bettersanic_data.type == "exception"]

        return new_cls


class BetterSanic(Sanic):
    def add_cog(self, cog):
        for route in cog.routes:
            data = route._bettersanic_data
            self.add_route(route, data.location, *data.args, **data.kwargs)
        for exception in cog.exceptions:
            data = exception._bettersanic_data
            for exception_type in data.exceptions:
                self.error_handler.add(
                    exception_type, exception, **data.kwargs)

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
