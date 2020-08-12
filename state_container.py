from threading import Lock, Thread
from typing import Dict, Any

class Singleton(type):
    _instances = {}
    _locks: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._locks:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StateContainerError(Exception):
    pass


class StateContainer(metaclass=Singleton):
    _state: Dict[str, Any] = {}

    def __init__(self):
        pass

    def add_value(self, key: str, value: Any) -> None:
        self._state.update({key: value})

    def get_value(self, key: str) -> Any:
        try:
            return self._state[key]
        except KeyError:
            raise StateContainerError(
        'Key {key} does not exist'.format(key=key)
        )

    def update(self, exisiting_dict: Dict[str, Any]) -> None:
        self._state.update(exisiting_dict)

    def keys(self):
        return self._state.keys()

    def items(self):
        return self._state.items()

    def __getitem__(self, key: str):
        return self._state[key]

    def __setitem__(self, key:str, value: Any):
        self._state[key] = value

# TESTING ENVIROMENT
# -----------------------------------------------------------------------------

def test_singleton_first_time(key:str, value: Any) -> None:
    singleton = StateContainer()
    singleton.add_value(key, value)
    print(singleton.get_value(key))

def test_singleton_another_time(key: str) -> None:
    singleton = StateContainer()
    print(singleton.get_value(key))
