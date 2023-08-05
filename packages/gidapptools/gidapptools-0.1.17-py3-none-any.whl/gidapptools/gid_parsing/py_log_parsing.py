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

from gidapptools.gid_parsing.universal.character_elements import BaseElements, Ligatures
from gidapptools.gid_parsing.universal.datetime_elements import get_grammar_from_dt_format

import pyparsing as ppa
import pyparsing.common as ppc
import pp
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion[Constants]


class GeneralGrammar:
    _cached_grammar: ppa.ParserElement = None

    @property
    def ___grammar___(self) -> ppa.ParserElement:
        if self._cached_grammar is None:
            self.__class__._cached_grammar = self._construct_grammar()
        return self._cached_grammar

    def _construct_grammar(self):
        non_pipe_printables = ppa.printables.replace("|", "")
        time_stamp_part = get_grammar_from_dt_format("%Y-%m-%d %H:%M:%S.%f %Z")("time_stamp")
        line_number_part = ppa.Word(ppa.nums)("line_number")
        level_part = (ppa.Keyword("DEBUG") | ppa.Keyword("INFO") | ppa.Keyword("CRITICAL") | ppa.Keyword("ERROR"))("level")
        thread_name_part = ppa.Word(non_pipe_printables)("thread")
        module_part = ppa.Word(non_pipe_printables)("module")
        function_part = ppa.Word(non_pipe_printables)("function")
        return time_stamp_part + BaseElements.pipe + line_number_part + BaseElements.pipe + level_part + BaseElements.pipe + thread_name_part + BaseElements.pipe + \
            module_part + BaseElements.pipe + function_part + BaseElements.pipe + BaseElements.pipe + Ligatures.big_arrow_right + ppa.rest_of_line("message")

# region[Main_Exec]


if __name__ == '__main__':
    x = """2022-01-16 00:34:48.328 CET |  108  |  DEBUG   |      MainThread      | gui.status_bar                      | _refresh_text_helper                ||--> refreshing LastUpdatedLabel(interval='30 seconds', last_triggered='2022-01-15 23:34:48 UTC') text"""
    g = GeneralGrammar()
    r = g.___grammar___.parse_string(x, parse_all=True)
    pp(r.as_dict())

# endregion[Main_Exec]
