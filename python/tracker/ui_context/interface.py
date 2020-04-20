import abc
from typing import Any, Sequence, Callable

from kivy.uix.widget import Widget


__all__ = ['UIContext']


class UIContext(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_screen_on(self) -> bool:
        pass

    @abc.abstractmethod
    def turn_on_screen(self) -> None:
        pass

    @abc.abstractmethod
    def turn_off_screen(self) -> None:
        pass

    @abc.abstractmethod
    def create_buttons(self, num: int, font_size: int, handler: Callable[[int], None]) -> Sequence[Widget]:
        pass

    def __enter__(self) -> None:
        self.turn_on_screen()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.turn_on_screen()
