from pathlib import Path

from .ui_context import UIContext
from .app import TrackerApp
from .data_saver import SqliteDataSaver


__all__ = ['run_for_context']


def run_for_context(context: UIContext) -> None:
    pages = [
        ['Fed Cat', 'Fed Baby', 'Pee'],
        ['Poo', 'Sleep start', 'Sleep end'],
    ]
    all_labels = [event for page in pages for event in page]
    app = TrackerApp(
        ui_context=context,
        data_saver=SqliteDataSaver(Path(__file__).parents[2] / 'tracker.sqlite', all_labels),
        num_buttons=4,
        next_page_button=3,
        pages=pages,
    )
    with app:
        app.run()
