"""
An interface for implementing a battery device driver for the CETONI SiLA SDK

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 18.05.2022
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Generator, Optional, Tuple

logger = logging.getLogger(__name__)


class BatteryInterface(ABC):
    """
    Interface for a battery device driver
    """

    _is_connected: bool = False
    _is_secondary_source_connected: bool = False
    _voltage: float = 0
    _temperature: float = 0
    _locking_pin_state: str = ""

    def __init__(self):
        super().__init__()

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def is_secondary_source_connected(self) -> bool:
        """
        Whether there is another power source that can be used to cover the time where the battery is not connected
        """
        return self._is_secondary_source_connected

    @property
    def voltage(self) -> float:
        return self._voltage

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def locking_pin_state(self) -> str:
        return self._locking_pin_state

    @abstractmethod
    def replace_battery(self) -> Optional[Generator[Tuple[int, str, bool], None, None]]:
        """
        Perform a battery replacement routine (e.g. perform steps so that the user can safely remove the battery and
        insert a new battery)

            :return: A generator with status information of the replacement routine (if available)
                     The generators yielded values are tuples with 3 elements where the first corresponds to the overall
                     progress (0 - 100), the seconds corresponds to a status message (`str`) and the third indicates whether
                     there was en error or not (`bool`)
        """
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        """
        Can be used to stop polling for battery value changes if active polling is used by the specific driver
        implementation
        """
        raise NotImplementedError()


class BatteryReplacementFailed(Exception):
    """
    An exception indicating that the battery replacement could not be performed (e.g. because of a failed precondition
    or a hardware error)
    """

    def __init__(self, msg: str = "Could not perform battery replacement") -> None:
        super().__init__(msg)
