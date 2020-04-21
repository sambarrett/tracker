#!/usr/bin/env python3

import abc
import datetime
from pathlib import Path
import sqlite3
from type import TracebackType
from typing import Optional, Any, List, Dict, Type

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.uix.widget import Widget


class Tracker(Widget):
    button_labels = ListProperty([str(x) for x in range(4)])
    button_infos = ListProperty([str(x) for x in range(4)])
    next_page_button: int = 3
    pages: List[List[str]] = [
        ['Fed Cat', 'Fed Baby', 'Pee'],
        ['Poo', 'Sleep start', 'Sleep end'],
    ]
    occurrences: Dict[str, List[datetime.datetime]]
    page: int = 0

    def __init__(self):
        super().__init__()
        self.occurrences = {label: [] for page in self.pages for label in page}
        self.setup_page()
        self.db_path = Path(__file__).parent / 'tracker.db'
        self.db_conn = sqlite3.connect(str(self.db_path))
        self.db_cursor = self.db_conn.cursor()

    def _create_table(self) -> None:
        print('Creating DB')
        self.db_cursor.execute('''CREATE TABLE events
                                  (type INT, time DATETIME)''')
        self.db_conn.commit()

    def _check_for_table(self) -> None:
        self.db_cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\' and name=\'events\'')
        res = self.db_cursor.fetchone()
        print(res)

    def insert_event(self) -> None:
        self.db_cursor.execute('INSERT INTO events VALUES ')

    def button_press(self, button: int) -> None:
        GPIO.output(18, 1023)  # turn on screen
        self.backlight_off_trigger.cancel()  # abort the previous one
        self.backlight_off_trigger()
        if self.screen_on:
            if button == self.next_page_button:
                self.page = (self.page + 1) % len(self.pages)
            else:
                if button > self.next_page_button:
                    page_ind = button - 1
                else:
                    page_ind = button
                label = self.pages[self.page][page_ind]
                self.occurrences[label].append(datetime.datetime.now())
            # for i in range(len(self.button_labels)):
            #     self.button_labels[i] = f'last {i}' if i == button else str(i)
        else:
            self.page = 0  # always reset the page
            self.screen_on = True
        self.setup_page()

    def setup_page(self) -> None:
        page_ind = 0
        for i in range(len(self.button_labels)):
            if i == self.next_page_button:
                self.button_infos[i] = f'Page {self.page + 1} / {len(self.pages)}'
                self.button_labels[i] = 'Next page'
            else:
                label = self.pages[self.page][page_ind]
                last = 'Never' if len(self.occurrences[label]) == 0 else self.occurrences[label][-1].strftime('%m/%d: %H:%M')
                self.button_infos[i] = f'Count: {len(self.occurrences[label])} Last: {last}'
                self.button_labels[i] = label
                page_ind += 1



class TrackerApp(App):
    tracker: Optional[Tracker] = None
    def build(self) -> Widget:
        self.tracker = Tracker()
        return self.tracker


if __name__ == '__main__':
    Window.fullscreen = True
    app = TrackerApp()
    # initialize the GPIO buttons
    GPIO.setmode(GPIO.BCM)
    button_codes = [17, 22, 23, 27]
    # initialize the backlight
    backlight_code = 18
    GPIO.setup(backlight_code, GPIO.OUT)
    try:
        def callback(x):
            # GPIO.output(backlight_code, 1023)  # turn on the screen
            up = GPIO.input(x)
            k = button_codes.index(x)
            if up:
                app.tracker.button_press(k)
            # if up:
            #     if k in app.tracker.buttons_down:
            #         app.tracker.buttons_down.remove(k)
            # else:
            #     app.tracker.buttons_down.add(k)
            # app.tracker.text = str(app.tracker.buttons_down)
        
        for i, button_code in enumerate(button_codes):
            GPIO.setup(button_code, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(button_code, GPIO.BOTH, callback=callback, bouncetime=50)

        app.run()
    finally:
        # turn the screen on at the end
        GPIO.output(backlight_code, 1023)
