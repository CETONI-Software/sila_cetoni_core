# Generated by sila2.code_generator; sila2.__version__: 0.10.1
# -----
# This class does not do anything useful at runtime. Its only purpose is to provide type annotations.
# Since sphinx does not support .pyi files (yet?), so this is a .py file.
# -----

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from typing import Iterable, Optional

    from shutdowncontroller_types import PrepareShutdown_Responses, Shutdown_Responses
    from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance


class ShutdownControllerClient:
    """

    Provides a generic way of telling a SiLA2 server that it is about to be shut down or to shut down itself. The server implements a routine to be executed before the hardware is shut down (e.g. saving device parameters or bringing the device into a safe position) and may also be capable of shutting itself down completely.

    """

    def PrepareShutdown(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[PrepareShutdown_Responses]:
        """

        Initiates the pre-shutdown routine. If no errors occurred during this process the server should be considered ready to be physically shutdown (i.e. the device can be shut down/powered off). Shutting down the server must be done manually, e.g. by unplugging the power to the device.

        """
        ...

    def Shutdown(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[Shutdown_Responses]:
        """

        Initiates the shutdown routine. This first executes the pre-shutdown routine (to store parameters, bring the device in a safe position, etc.) and then physically shuts down the device. If errors occurred during the pre-shutdown process the server is considered not ready to be physically shutdown (i.e. the device will not be shut down/powered off).

        """
        ...
