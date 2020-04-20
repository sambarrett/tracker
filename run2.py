#!/usr/bin/env python3

from pathlib import Path

from tracker import ui_context, SqliteDataSaver
from tracker.app import TrackerApp

if __name__ == '__main__':
    pages = [
        ['Fed Cat', 'Fed Baby', 'Pee'],
        ['Poo', 'Sleep start', 'Sleep end'],
    ]
    all_labels = [event for page in pages for event in page]
    app = TrackerApp(
        ui_context=ui_context.Computer(),
        data_saver=SqliteDataSaver(Path(__file__).parent / 'tracker.sqlite', all_labels),
        num_buttons=4,
        next_page_button=3,
        pages=pages,
    )
    with app:
        app.run()
