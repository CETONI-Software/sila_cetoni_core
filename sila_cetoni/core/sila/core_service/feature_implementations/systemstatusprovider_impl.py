# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

from concurrent.futures import Executor

from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem
from sila_cetoni.utils import PropertyUpdater, not_equal

from ..generated.systemstatusprovider import SystemStatusProviderBase
from ..server import Server


@CetoniApplicationSystem.monitor_traffic
class SystemStatusProviderImpl(SystemStatusProviderBase):
    __system: ApplicationSystem

    def __init__(self, server: Server):
        super().__init__(server)
        self.__system = ApplicationSystem()  # type: ignore

        self.run_periodically(PropertyUpdater(lambda: self.__system.state.value, not_equal, self.update_SystemState))
