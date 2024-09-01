from __future__ import annotations
from .logger import CustomLogger


class Registrar(type):
    """Metaclass for registering classes."""
    registry = {}

    def __new__(cls, name, bases, dct) -> Registrar:
        # Create the new class as usual
        new_class = super().__new__(cls, name, bases, dct)
        # Register the new class
        cls.registry[name] = new_class
        return new_class

    @classmethod
    def get(cls, name: str) -> Registrar:
        return cls.registry.get(name)

    @classmethod
    def get_all(cls) -> dict[str, Registrar]:
        return cls.registry

    @classmethod
    def clear(cls) -> None:
        cls.registry.clear()

    def __repr__(self) -> str:
        return f"{self.__name__}({self.registry})"


class Base(metaclass=Registrar):
    """Base class for all classes in the library."""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.logger = CustomLogger(name=cls.__name__, debug=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
