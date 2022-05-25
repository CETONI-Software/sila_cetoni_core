"""
An interface for implementing a battery device driver for the CETONI SiLA SDK

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 18.05.2022
"""

from __future__ import annotations

import logging

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BatteryInterface(ABC):
    """
    Interface for a battery device driver
    """

    _voltage: float
    _temperature: float
    _locking_pin_state: str

    def __init__(self):
        super().__init__()

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
    def replace_battery(self):
        """
        Perform a battery replacement routine (e.g. perform steps so that the user can safely remove the battery and
        insert a new battery)
        """
        raise NotImplementedError()


class BatteryReplacementFailed(Exception):
    """
    An exception indicating that the battery replacement could not be performed (e.g. because of a failed precondition
    or a hardware error)
    """

    def __init__(self, msg: str = "Could not perform battery replacement") -> None:
        super().__init__(msg)
