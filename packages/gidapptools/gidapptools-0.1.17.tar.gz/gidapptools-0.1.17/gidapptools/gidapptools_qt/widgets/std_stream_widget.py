"""
WiP.

Soon.
"""

# region [Imports]

import os
import re
import sys
import json
import queue
import math
import base64
import pickle
import random
import shelve
import dataclasses
import shutil
import asyncio
import logging
import sqlite3
import platform
import importlib
import subprocess
import inspect
from threading import Thread
from time import sleep, process_time, process_time_ns, perf_counter, perf_counter_ns
from io import BytesIO, StringIO
from abc import ABC, ABCMeta, abstractmethod
from copy import copy, deepcopy
from enum import Enum, Flag, auto, unique
from time import time, sleep
from pprint import pprint, pformat
from pathlib import Path
from string import Formatter, digits, printable, whitespace, punctuation, ascii_letters, ascii_lowercase, ascii_uppercase
from timeit import Timer
from typing import TYPE_CHECKING, Union, Callable, Iterable, Optional, Mapping, Any, IO, TextIO, BinaryIO, Hashable, Generator, Literal, TypeVar, TypedDict, AnyStr
from zipfile import ZipFile, ZIP_LZMA
from datetime import datetime, timezone, timedelta
from tempfile import TemporaryDirectory
from textwrap import TextWrapper, fill, wrap, dedent, indent, shorten
from functools import wraps, partial, lru_cache, singledispatch, total_ordering, cached_property
from importlib import import_module, invalidate_caches
from contextlib import contextmanager, asynccontextmanager, nullcontext, closing, ExitStack, suppress
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from urllib.parse import urlparse
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from importlib.machinery import SourceFileLoader

import PySide6


from PySide6.QtCore import QObject, Signal


from PySide6.QtWidgets import QApplication, QFrame, QGridLayout, QLabel, QTextEdit, QWidget

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion[Constants]


class StreamTypus(Enum):
    STDOUT = "stdout"
    STDERR = "stderr"


class BaseStdStreamCapturer:

    def __init__(self, stream_typus: Union["StreamTypus", str], signaler=None) -> None:
        self._stream_typus = StreamTypus(stream_typus)
        self._original_stream = None
        self.installed: bool = False
        self.signaler = signaler
        self.text_items: list[str] = []

    @property
    def stream_typus(self) -> "StreamTypus":
        return self._stream_typus

    @property
    def original_stream(self):
        return self._original_stream

    def write(self, text: str):
        self.text_items.append(text)
        if self.signaler is not None:
            self.signaler.updated.emit(self.get_text())

    def flush(self):
        pass

    def get_text(self) -> str:
        return ''.join(self.text_items)

    def clear(self):
        self.text_items.clear()

    def install(self):
        if self.stream_typus is StreamTypus.STDOUT:
            self._original_stream = sys.stdout
            sys.stdout = self

        elif self.stream_typus is StreamTypus.STDERR:
            self._original_stream = sys.stderr
            sys.stderr = self

        else:
            raise TypeError(f"Unknown stream-typus {self.stream_typus!r}")

        self.installed = True

    def uninstall(self):
        if self.stream_typus is StreamTypus.STDOUT:
            sys.stdout = self.original_stream
            self._original_stream = None

        elif self.stream_typus is StreamTypus.STDERR:
            sys.stderr = self.original_stream
            self._original_stream = None

        else:
            raise TypeError(f"Unknown stream-typus {self.stream_typus!r}")

        self.installed = False


class StdoutCapturer(BaseStdStreamCapturer):

    def __init__(self, signaler=None) -> None:
        super().__init__(stream_typus=StreamTypus.STDOUT, signaler=signaler)


class StderrCapturer(BaseStdStreamCapturer):

    def __init__(self, signaler=None) -> None:
        super().__init__(stream_typus=StreamTypus.STDERR, signaler=signaler)


class Signaler(QObject):
    updated = Signal(str)


class StdStreamWidget(QWidget):
    capturer_classes: dict[StreamTypus, type[BaseStdStreamCapturer]] = {StreamTypus.STDOUT: StdoutCapturer,
                                                                        StreamTypus.STDERR: StderrCapturer}

    def __init__(self, stream_typus: Union["StreamTypus", str], parent: Optional[PySide6.QtWidgets.QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.signaler = Signaler()
        self.capturer = self.capturer_classes[StreamTypus(stream_typus)](signaler=self.signaler)

        self.setLayout(QGridLayout())
        self.text_view: QTextEdit = None

    def setup(self) -> "StdStreamWidget":
        self.title_label = QLabel()
        self.title_label.setText(self.capturer.stream_typus.value.title())
        self.title_label.setFrameShape(QFrame.WinPanel)
        self.layout.addWidget(self.title_label)

        self.capturer.install()

        self.text_view = QTextEdit(self)
        self.text_view.setReadOnly(True)
        self.layout.addWidget(self.text_view)
        self.signaler.updated.connect(self.text_view.setPlainText)

        return self

    @property
    def layout(self) -> QGridLayout:
        return super().layout()


# region[Main_Exec]
if __name__ == '__main__':
    def print_shit():
        for shit in ["this", "is", "stuff", "printed", "to", "stdout"]:
            print(shit)
            sleep(5)

    app = QApplication()
    w = StdStreamWidget(StreamTypus.STDOUT).setup()
    w.show()
    t = Thread(target=print_shit)
    t.start()
    sys.exit(app.exec())

# endregion[Main_Exec]
