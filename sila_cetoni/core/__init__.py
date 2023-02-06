from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from sila_cetoni.application.application_configuration import ApplicationConfiguration

from sila_cetoni.application.device import Device

from .sila.core_service.server import Server

logger = logging.getLogger(__name__)


def parse_devices(json_devices: Optional[Dict[str, Dict]]) -> List[Device]:
    """
    Parses the given JSON configuration `json_devices` and creates the necessary `Device`s

    Parameters
    ----------
    json_devices: Dict[str, Dict] (optional)
        The `"devices"` section of the JSON configuration file as a dictionary (key is the device name, the value is a
        dictionary with the configuration parameters for the device, i.e. `"type"`, `"manufacturer"`, ...)

    Returns
    -------
    List[Device]
        A list with all `Device`s as defined in the JSON config
    """
    # no physical devices for the core features
    return []


def create_devices(config: ApplicationConfiguration, scan: bool = False) -> None:
    """
    Looks up all core devices from the current configuration and tries to auto-detect more devices if `scan` is `True`

    Parameters
    ----------
    config: ApplicationConfiguration
        The application configuration containing all devices for which SiLA Server and thus device driver instances
        shall be created
    scan: bool (default: False)
        Whether to scan for more devices than the ones defined in `config`
    """
    # no physical devices for the core features
    pass


def create_server(device: Device, **server_args) -> Server:
    """
    Creates the SiLA Server for the given `device`

    Parameters
    ----------
    device: Device
        The device for which to create a SiLA Server
    **server_args
        Additional arguments like server name, server UUID to pass to the server's `__init__` function
    """
    # no standalone SiLA Servers for the core features
    pass
