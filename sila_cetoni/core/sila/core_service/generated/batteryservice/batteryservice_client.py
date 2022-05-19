# Generated by sila2.code_generator; sila2.__version__: 0.8.0
# -----
# This class does not do anything useful at runtime. Its only purpose is to provide type annotations.
# Since sphinx does not support .pyi files (yet?), so this is a .py file.
# -----

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from typing import Iterable, Optional

    from batteryservice_types import PerformBatteryReplacement_Responses
    from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance, ClientObservableProperty


class BatteryServiceClient:
    """
    Provides information on the state of a battery and allows initiating a battery replacement routine
    """

    BatteryVoltage: ClientObservableProperty[float]
    """
    The current voltage of the battery
    """

    BatteryTemperature: ClientObservableProperty[int]
    """
    The current temperature of the battery block
    """

    LockingPinState: ClientObservableProperty[str]
    """
    The state of the locking pin that holds the battery in its place
    """

    def PerformBatteryReplacement(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[PerformBatteryReplacement_Responses]:
        """
        Performs the battery replacement routine, i.e. unlocks the battery block, waits until the old battery has been removed and the new one has been inserted and locks the battery block again.
        """
        ...
