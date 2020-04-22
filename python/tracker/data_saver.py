import abc
from datetime import datetime
from pathlib import Path
import sqlite3
from typing import Sequence, Dict, Optional, Any, Mapping

import dateutil.parser as datetime_parser
import pytz

__all__ = ['DataSaver', 'SqliteDataSaver']


class DataSaver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert_event(self, event_name: str) -> None:
        pass

    @abc.abstractmethod
    def get_last_occurrences(self, event_names: Sequence[str]) -> Mapping[str, Optional[datetime]]:
        pass

    @abc.abstractmethod
    def get_num_in_last_24_hours(self, event_names: Sequence[str]) -> Mapping[str, int]:
        pass

    @abc.abstractmethod
    def __enter__(self) -> None:
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


class SqliteDataSaver(DataSaver):
    _db_path: Path
    _db_conn: Optional[sqlite3.Connection]
    _db_cursor: Optional[sqlite3.Cursor]
    _event_name_to_id: Dict[str, int]
    _event_id_to_name: Dict[int, str]
    _event_names: Sequence[str]
    _timezone: pytz.tzinfo.DstTzInfo

    def __init__(self, db_path: Path, event_names: Sequence[str]):
        self._db_path = db_path
        self._event_name_to_id = {}
        self._event_id_to_name = {}
        self._event_names = event_names
        self._timezone = pytz.timezone('US/Eastern')

    def __enter__(self) -> None:
        self._db_conn = sqlite3.connect(str(self._db_path))
        self._db_cursor = self._db_conn.cursor()
        if not self._event_name_to_id:
            self._create_table()
            self._set_event_name_to_id()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._db_conn.close()
        self._db_conn = None
        self._db_cursor = None

    def _create_table(self) -> None:
        self._db_cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                                      type INT NOT NULL,
                                      time DATETIME NOT NULL
                                    );''')
        self._db_cursor.execute('''CREATE TABLE IF NOT EXISTS event_types (
                                        name TEXT NOT NULL
                                    );''')
        self._db_conn.commit()

    def _set_event_name_to_id(self) -> None:
        for event_name in self._event_names:
            select = ('SELECT rowid FROM event_types WHERE name = ?;', (event_name,))
            self._db_cursor.execute(*select)
            res = self._db_cursor.fetchone()
            if res is None:
                self._db_cursor.execute('INSERT INTO event_types (name) VALUES (?);', (event_name,))
                self._db_conn.commit()
                self._db_cursor.execute(*select)
                res = self._db_cursor.fetchone()
            self._event_name_to_id[event_name] = res[0]
            self._event_id_to_name[res[0]] = event_name

    # def _table_exists(self) -> bool:
    #     self._db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='events'")
    #     res = self._db_cursor.fetchone()
    #     return res is not None

    def insert_event(self, event_name: str) -> None:
        assert self._db_conn
        assert event_name in self._event_name_to_id
        self._db_cursor.execute("INSERT INTO events (type, time) VALUES (?, DATETIME('now'));",
                                (self._event_name_to_id[event_name], ))
        self._db_conn.commit()

    def get_last_occurrences(self, event_names: Sequence[str]) -> Mapping[str, Optional[datetime]]:
        assert self._db_conn
        event_ids = [self._event_name_to_id[event_name] for event_name in event_names]
        self._db_cursor.execute('SELECT type, max(time) as latest FROM events GROUP BY type;')
        rows = self._db_cursor.fetchall()
        res = {}
        for eid, dt in rows:
            if eid in event_ids:
                event_name = self._event_id_to_name[eid]
                res[event_name] = pytz.utc.localize(datetime_parser.isoparse(dt)).astimezone(self._timezone)
        for event_name in event_names:
            if event_name not in res:
                res[event_name] = None
        return res

    def get_num_in_last_24_hours(self, event_names: Sequence[str]) -> Mapping[str, int]:
        assert self._db_conn
        event_ids = [self._event_name_to_id[event_name] for event_name in event_names]
        self._db_cursor.execute("SELECT type, COUNT(*) as count "
                                "FROM events "
                                "WHERE time > DATETIME('now', '-1 day') "
                                "GROUP BY type;")
        rows = self._db_cursor.fetchall()
        res = {}
        for eid, count in rows:
            if eid in event_ids:
                event_name = self._event_id_to_name[eid]
                res[event_name] = count
        for event_name in event_names:
            if event_name not in res:
                res[event_name] = 0
        return res
