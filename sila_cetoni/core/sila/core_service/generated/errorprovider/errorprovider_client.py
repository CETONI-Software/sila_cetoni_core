# Generated by sila2.code_generator; sila2.__version__: 0.10.1
# -----
# This class does not do anything useful at runtime. Its only purpose is to provide type annotations.
# Since sphinx does not support .pyi files (yet?), so this is a .py file.
# -----

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, List, Optional

    from errorprovider_types import ClearAllErrors_Responses
    from sila2.client import ClientMetadataInstance, ClientObservableProperty


class ErrorProviderClient:
    """
    This feature provides global error functionality that a client can subscribe to to get notified about any errors of the server without having to execute a Command, read a Property or (re-)start a Property subscription.
    """

    Errors: ClientObservableProperty[List[Error]]
    """
    The list of errors that occurred during the lifetime of this server or since the last time ClearAllErrors was called.
    """

    LastError: ClientObservableProperty[Error]
    """
    The most recent error that occurred.
    """

    def ClearAllErrors(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClearAllErrors_Responses:
        """
        Clears all errors
        """
        ...