from typing import Any, Sequence, Callable

from kivy.uix.button import Button

from .interface import UIContext


__all__ = ['Computer']


class Computer(UIContext):
    def is_screen_on(self) -> bool:
        return True

    def turn_on_screen(self) -> None:
        pass

    def turn_off_screen(self) -> None:
        pass

    def create_buttons(self, num: int, font_size: int, handler: Callable[[int], None]) -> Sequence[Button]:
        buttons = [Button(font_size=font_size, text=str(i)) for i in range(num)]
        for i, button in enumerate(buttons):
            button.bind(on_press=lambda _, i=i: handler(i))
        return buttons

    def __enter__(self) -> None:
        self.turn_on_screen()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.turn_on_screen()
