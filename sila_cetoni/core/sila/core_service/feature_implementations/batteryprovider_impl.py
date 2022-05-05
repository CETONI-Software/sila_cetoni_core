from __future__ import annotations

import math
import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict

from qmixsdk.qmixanalogio import AnalogInChannel
from sila2.framework import FullyQualifiedIdentifier

from sila_cetoni.application.system import ApplicationSystem

from ..generated.batteryprovider import BatteryProviderBase


class BatteryProviderImpl(BatteryProviderBase):
    __system: ApplicationSystem
    __channel: AnalogInChannel
    __stop_event: Event

    def __init__(self, executor: Executor):
        super().__init__()
        self.__system = ApplicationSystem()
        # The only battery powered device we have is our mobile dosage unit (MobDos).
        # This will always only have a single pump where the first analog in channel
        # provides the current voltage of the system (i.e. the voltage of the battery).
        self.__channel = self.__system.pumps[0].io_channels[0]
        self.__stop_event = Event()

        # The value we get from the analog in channel has been divided by
        # a voltage divider so we have to multiply by this factor to get
        # the actual voltage value.
        VOLTAGE_DIVIDER_FACTOR = 0.00558

        def update_voltage(stop_event: Event):
            new_voltage = voltage = (
                self.__channel.read_input() * VOLTAGE_DIVIDER_FACTOR if self.__system.state.is_operational() else 0
            )
            while not stop_event.is_set():
                new_voltage = (
                    self.__channel.read_input() * VOLTAGE_DIVIDER_FACTOR if self.__system.state.is_operational() else 0
                )
                if not math.isclose(new_voltage, voltage, abs_tol=1.0e-3):
                    voltage = new_voltage
                    self.update_BatteryVoltage(voltage)
                time.sleep(0.1)

        # initial value
        self.update_BatteryVoltage(self.__channel.read_input() * VOLTAGE_DIVIDER_FACTOR)

        executor.submit(update_voltage, self.__stop_event)

    def stop(self) -> None:
        self.__stop_event.set()