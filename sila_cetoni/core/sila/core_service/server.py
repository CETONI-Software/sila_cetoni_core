import logging
from typing import Optional, Union
from uuid import UUID

from sila2.server import SilaServer

from ...device_drivers.abc import BatteryInterface
from .feature_implementations.batteryservice_impl import BatteryServiceImpl
from .feature_implementations.systemstatusprovider_impl import SystemStatusProviderImpl
from .generated.batteryservice import BatteryServiceFeature
from .generated.systemstatusprovider import SystemStatusProviderFeature

logger = logging.getLogger(__name__)


__version__ = "1.0.0"


class Server(SilaServer):
    def __init__(
        self,
        battery: Optional[BatteryInterface] = None,
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        super().__init__(
            server_name=server_name or "Core Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "Provides status information about the overall system",
            server_version=server_version or __version__,
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
            max_child_task_workers=1000,
            max_grpc_workers=1000,
        )

        self.systemstatusprovider = SystemStatusProviderImpl(self, self.child_task_executor)
        self.set_feature_implementation(SystemStatusProviderFeature, self.systemstatusprovider)

        if battery is None:
            logger.debug("This device does not have a battery")
            return

        self.batteryprovider = BatteryServiceImpl(self, battery, self.child_task_executor)
        self.set_feature_implementation(BatteryServiceFeature, self.batteryprovider)
