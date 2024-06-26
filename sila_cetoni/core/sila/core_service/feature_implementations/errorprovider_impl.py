# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from queue import Queue
from typing import TYPE_CHECKING, ClassVar, List

from sila2.server import MetadataDict

from sila_cetoni.utils import PropertyUpdater, not_equal

from ..generated.errorprovider import ClearAllErrors_Responses
from ..generated.errorprovider import Error as ErrorType
from ..generated.errorprovider import ErrorProviderBase
from ..generated.errorprovider import SeverityLevel as SeverityLevelType

if TYPE_CHECKING:
    from ..server import Server

logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    INFO = "Info"
    WARNING = "Warning"
    CRITICAL = "Critical"
    FATAL = "Fatal"


@dataclass(frozen=True)
class Error:
    level: SeverityLevel
    description: str
    timestamp: datetime = field(default_factory=lambda: datetime.now().astimezone())

    NO_ERROR_DESCRIPTION: ClassVar[str] = "No error"
    RESOLVED_ERROR_DESCRIPTION: ClassVar[str] = "No error - all previous errors have been resolved"

    def __level_to_code(self) -> int:
        if self.level == SeverityLevel.INFO:
            return 0
        if self.level == SeverityLevel.WARNING:
            return 1
        if self.level == SeverityLevel.CRITICAL:
            return 2
        if self.level == SeverityLevel.FATAL:
            return 3
        raise ValueError(f"Unknown severity level {self.level!r}")

    def to_error_type(self) -> ErrorType:
        return ErrorType(
            Timestamp=self.timestamp,
            Level=SeverityLevelType(Code=self.__level_to_code(), Name=self.level.value),
            Description=self.description,
        )

    def is_resolved_error(self) -> bool:
        """
        Returns whether this error represents a "No error" that indicates that all previous errors have been resolved
        """
        return self.level == SeverityLevel.INFO and self.description == self.RESOLVED_ERROR_DESCRIPTION

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.timestamp!s}, {self.level.value!r}, {self.description!r})"


class ErrorProviderImpl(ErrorProviderBase):
    __errors: deque[Error]
    __last_error: Error

    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

        self.__errors = deque(maxlen=10)
        self.__last_error = Error(SeverityLevel.INFO, Error.NO_ERROR_DESCRIPTION)

        self.run_periodically(
            PropertyUpdater(
                self.__errors.copy, not_equal, lambda errors: self.update_Errors([e.to_error_type() for e in errors])
            )
        )

    def update_Errors(self, errors: List, queue: Queue[List] | None = None) -> None:
        super().update_Errors(errors, queue)

        self.__last_error = (
            self.__errors[-1] if len(self.__errors) > 0 else Error(SeverityLevel.INFO, Error.NO_ERROR_DESCRIPTION)
        )
        self.update_LastError(self.__last_error.to_error_type())

    def ClearAllErrors(self, *, metadata: MetadataDict) -> ClearAllErrors_Responses:
        self.__errors.clear()
        return ClearAllErrors_Responses()

    # interface for other feature implementations
    def add_error(self, error: Error) -> None:
        """
        Adds an error to the list of errors
        """
        logger.debug(f"Received new error {error}")
        self.__errors.append(error)

    def resolve_error(self) -> None:
        """
        Adds a "No error" error to the list of errors indicating that the error(s) that occurred before are now resolved
        """
        self.add_error(Error(SeverityLevel.INFO, Error.RESOLVED_ERROR_DESCRIPTION))

    @property
    def errors(self) -> List[Error]:
        """
        The current list of errors
        """
        return list(self.__errors)

    @property
    def last_error(self) -> Error:
        """
        The error that occurred last
        """
        return self.__last_error


# ----------------------------------------------------------------------------
# test
if __name__ == "__main__":
    import time
    from copy import deepcopy
    from datetime import timedelta

    now = datetime.now()
    e1 = Error(SeverityLevel.INFO, "test 1", now)
    e2 = Error(SeverityLevel.INFO, "test 1", now)
    e3 = Error(SeverityLevel.WARNING, "test 1", now)
    e4 = Error(SeverityLevel.INFO, "test 2", now)
    e5 = Error(SeverityLevel.INFO, "test 1", now + timedelta(seconds=1))

    d1 = deque(maxlen=10)
    d1.append(e1)
    d1.append(e2)
    d1.append(e3)

    d2 = d1.copy()
    d3 = deepcopy(d1)

    print("d1", d1, id(d1), id(d1[0]), id(d1[1]), id(d1[2]))
    print("d2", d2, id(d2), id(d2[0]), id(d2[1]), id(d2[2]))
    print("d3", d3, id(d3), id(d3[0]), id(d3[1]), id(d3[2]))

    d1.append(e1)

    print("d1", d1, id(d1), id(d1[0]), id(d1[1]), id(d1[2]))
    print("d2", d2, id(d2), id(d2[0]), id(d2[1]), id(d2[2]))
    print("d3", d3, id(d3), id(d3[0]), id(d3[1]), id(d3[2]))

    print(d1 == d2)
    print(d1 == d3)
    print(d2 == d3)

    exit()

    print(e1)
    print(e2)
    print(e3)
    print(e4)
    print(e5)
    print(Error(SeverityLevel.CRITICAL, "test"))
    time.sleep(2)
    print(Error(SeverityLevel.FATAL, "test"))

    assert e1 == e2

    assert e1 != e3
    assert e2 != e3

    assert e1 != e4
    assert e2 != e4
    assert e3 != e4

    assert e1 != e5
    assert e2 != e5
    assert e3 != e5
    assert e4 != e5
