from typing import Any, Callable, Sequence

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
import RPi.GPIO as GPIO

from .interface import UIContext


__all__ = ['RPi']


class RPi(UIContext):
    _backlight_off_trigger: Any
    _backlight_code: int
    _screen_on: bool = True

    def __init__(self, backlight_code: int = 18):
        super().__init__()
        Window.fullscreen = True
        Window.size = (640, 480)

        self._backlight_code = backlight_code
        # initialize the GPIO buttons
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._backlight_code, GPIO.OUT)  # set up the channel
        # set up the trigger
        self._backlight_off_trigger = Clock.create_trigger(self.turn_off_screen, timeout=20.0)
        self._backlight_off_trigger()

    def is_screen_on(self) -> bool:
        return self._screen_on

    def turn_on_screen(self) -> None:
        GPIO.output(self._backlight_code, 1023)  # turn on screen
        self._screen_on = True
        self._backlight_off_trigger.cancel()  # abort the previous one
        self._backlight_off_trigger()

    def turn_off_screen(self, *args: Any) -> None:
        GPIO.output(self._backlight_code, 0)
        self._screen_on = False

    def create_buttons(self, num: int, font_size: int, handler: Callable[[int], None]) -> Sequence[Label]:
        button_codes = [17, 22, 23, 27]
        assert num == len(button_codes)
        for i, button_code in enumerate(button_codes):
            GPIO.setup(button_code, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            def f(button: int, i: int = i) -> None:
                handler(i)

            GPIO.add_event_detect(button_code, GPIO.RISING, callback=f, bouncetime=200)
        return [Label(text=str(i), font_size=font_size) for i in range(num)]

    def font_size(self) -> int:
        return 25
