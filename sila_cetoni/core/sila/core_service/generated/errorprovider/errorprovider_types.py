# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

from collections import namedtuple
from typing import Any, NamedTuple


class ClearAllErrors_Responses(NamedTuple):
    pass


SeverityLevel = namedtuple("SeverityLevel", ["Code", "Name"])

Error = namedtuple("Error", ["Timestamp", "Level", "Description"])