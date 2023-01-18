# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.server import MetadataDict, ObservableCommandInstance

from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem

from ..generated.shutdowncontroller import PrepareShutdown_Responses, Shutdown_Responses, ShutdownControllerBase

if TYPE_CHECKING:
    from ..server import Server


@CetoniApplicationSystem.monitor_traffic
class ShutdownControllerImpl(ShutdownControllerBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)

    def PrepareShutdown(
        self, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> PrepareShutdown_Responses:
        instance.begin_execution()  # set execution status from `waiting` to `running`
        # nothing to do here

    def Shutdown(self, *, metadata: MetadataDict, instance: ObservableCommandInstance) -> Shutdown_Responses:
        instance.begin_execution()  # set execution status from `waiting` to `running`
        self.PrepareShutdown()
        ApplicationSystem().shutdown()