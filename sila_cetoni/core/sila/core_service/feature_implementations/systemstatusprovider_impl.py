# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

import time
from concurrent.futures import Executor
from threading import Event

from sila2.server import SilaServer

from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem

from ..generated.systemstatusprovider import SystemStatusProviderBase


@CetoniApplicationSystem.monitor_traffic
class SystemStatusProviderImpl(SystemStatusProviderBase):
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, server: SilaServer, executor: Executor):
        super().__init__(server)
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_state(stop_event: Event):
            new_state = state = self.__system.state.value
            while not stop_event.is_set():
                new_state = self.__system.state.value
                if new_state != state:
                    state = new_state
                    self.update_SystemState(state)
                time.sleep(0.1)

        # initial value
        self.update_SystemState(self.__system.state.value)

        executor.submit(update_state, self.__stop_event)

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
