from typing import Sequence, List, Union, Any

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget

from .data_saver import DataSaver
from .ui_context import UIContext


class TrackerApp(App):
    _ui_context: UIContext
    _data_saver: DataSaver
    _num_buttons: int
    _next_page_button: int

    _pages: Sequence[Sequence[str]]
    _page_ind: int

    _layout: Layout
    _row_layouts: List[Layout]
    _counts: List[Label]
    _lasts: List[Label]
    _buttons: Sequence[Widget]

    def __init__(self, ui_context: UIContext,
                 data_saver: DataSaver,
                 num_buttons: int,
                 next_page_button: int,
                 pages: Sequence[Sequence[str]]):
        super().__init__()
        self._ui_context = ui_context
        self._data_saver = data_saver
        self._num_buttons = num_buttons
        assert 0 <= next_page_button < num_buttons
        self._next_page_button = next_page_button
        self._pages = pages
        for page in self._pages:
            assert len(page) <= num_buttons
        self._page_ind = 0

    def __enter__(self) -> None:
        self._ui_context.__enter__()
        # self._data_saver.__enter__()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # TODO I don't think this is quite right
        self._ui_context.__exit__(exc_type, exc_val, exc_tb)
        # self._data_saver.__exit__(exc_type, exc_val, exc_tb)

    def build(self) -> Widget:
        font_size = self._ui_context.font_size()
        self._layout = BoxLayout(orientation='vertical')
        self._layout.add_widget(BoxLayout(orientation='horizontal', size_hint=(1.0, 0.2)))  # offset
        self._row_layouts = [BoxLayout(orientation='horizontal') for _ in range(self._num_buttons)]
        self._counts = [Label(font_size=font_size, text=str(i)) for i in range(self._num_buttons)]
        self._lasts = [Label(font_size=font_size, text=str(i)) for i in range(self._num_buttons)]
        self._buttons = self._ui_context.create_buttons(self._num_buttons, font_size, self.process_button_ind)
        for i, (layout, count, last, button) in enumerate(zip(self._row_layouts, self._counts, self._lasts,
                                                              self._buttons)):
            self._layout.add_widget(layout)
            layout.add_widget(count)
            layout.add_widget(last)
            layout.add_widget(button)
        self._setup_page()
        return self._layout

    def process_button_ind(self, button: int) -> None:
        if self._ui_context.is_screen_on():
            if button == self._next_page_button:
                self._page_ind = (self._page_ind + 1) % len(self._pages)
            else:
                if button > self._next_page_button:
                    button_ind = button - 1
                else:
                    button_ind = button
                label = self._pages[self._page_ind][button_ind]
                with self._data_saver:
                    self._data_saver.insert_event(label)
        else:
            self._page_ind = 0  # always reset the page
        self._ui_context.turn_on_screen()
        self._setup_page()

    def _setup_page(self) -> None:
        button_ind = 0
        with self._data_saver:
            event_to_last = self._data_saver.get_last_occurrences(self._pages[self._page_ind])
            event_to_count = self._data_saver.get_num_in_last_24_hours(self._pages[self._page_ind])
        for i in range(len(self._buttons)):
            if i == self._next_page_button:
                self._counts[i].text = f'Page {self._page_ind + 1} / {len(self._pages)}'
                self._lasts[i].text = ''
                self._buttons[i].text = 'Next page'
            else:
                label = self._pages[self._page_ind][button_ind]
                self._counts[i].text = f'In last 24 hours: {event_to_count[label]}'
                last = 'Never' if event_to_last[label] is None else event_to_last[label].strftime('%m/%d: %H:%M')
                self._lasts[i].text = f'Last: {last}'
                self._buttons[i].text = label
                button_ind += 1
