#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SystemStatusProvider*

:details: SystemStatusProvider:
    Provides status information about the overall system

:file:    SystemStatusProvider_server.py
:authors: Florian Meinicke

:date: (creation)          2021-07-15T09:24:07.999138
:date: (last modification) 2021-07-15T09:24:07.999138

.. note:: Code generated by sila2codegenerator 0.3.6

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

import os
import logging
import argparse
from sys import meta_path

# Import the main SiLA library
from sila2lib.sila_server import SiLA2Server

# Import gRPC libraries of features
from impl.de.cetoni.core.SystemStatusProvider.gRPC import SystemStatusProvider_pb2
from impl.de.cetoni.core.SystemStatusProvider.gRPC import SystemStatusProvider_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.core.SystemStatusProvider.SystemStatusProvider_default_arguments import default_dict as SystemStatusProvider_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.core.SystemStatusProvider.SystemStatusProvider_servicer import SystemStatusProvider

# optional hardware interface communication
# from sila2comlib.com.com_serial import ComSerial

from ..local_ip import LOCAL_IP


class SystemStatusProviderServer(SiLA2Server):
    """
    Provides status information about the overall system
    """

    def __init__(self, cmd_args, simulation_mode: bool = True):
        """Class initialiser"""
        super().__init__(
            name=cmd_args.server_name, description=cmd_args.description,
            server_type=cmd_args.server_type, server_uuid=None,
            version=__version__,
            vendor_url="cetoni.de",
            ip=LOCAL_IP, port=int(cmd_args.server_port),
            key_file=cmd_args.encryption_key, cert_file=cmd_args.encryption_cert,
            meta_path=cmd_args.meta_dir,
            simulation_mode=simulation_mode,
            max_worker_threads=1000
        )

        self.simulation_mode = simulation_mode

        meta_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..',
                                                 'features', 'de', 'cetoni', 'core'))

        logging.info(
            "Starting SiLA2 server with server name: {server_name}".format(
                server_name=cmd_args.server_name
            )
        )

        # registering features
        #  Register SystemStatusProvider
        self.SystemStatusProvider_servicer = SystemStatusProvider(simulation_mode=self.simulation_mode)
        SystemStatusProvider_pb2_grpc.add_SystemStatusProviderServicer_to_server(
            self.SystemStatusProvider_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='de.cetoni/core/SystemStatusProvider/v1',
                         servicer=self.SystemStatusProvider_servicer,
                         meta_path=meta_path)

def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: SystemStatusProvider")

    # simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="SystemStatusProvider", help='start SiLA server with SiLA server name [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with SiLA server type [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="Provides status information about the overall system", help='SiLA server description')

    parser.add_argument('-m', '--meta-dir', action='store', default='meta',
                        help='Path to meta data directory for FDL and .proto files.')

    # connection parameters
    parser.add_argument('-i', '--server-ip-address', action='store', default='127.0.0.1',
                        help='SiLA server IP address')
    parser.add_argument('--server-hostname', action='store', default='localhost',
                        help='SiLA server hostname')
    parser.add_argument('-p', '--server-port', action='store', default=50052,
                        help='SiLA server port')

    # encryption
    parser.add_argument('-X', '--encryption', action='store', default=None,
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parsed_args = parser.parse_args()

    # validate/update some settings
    #   encryption
    if parsed_args.encryption is not None:
        # only overwrite the separate keys if not given manually
        if parsed_args.encryption_key is None:
            parsed_args.encryption_key = parsed_args.encryption + '.key'
        if parsed_args.encryption_cert is None:
            parsed_args.encryption_cert = parsed_args.encryption + '.cert'

    return parsed_args


if __name__ == '__main__':
    # or use logging.ERROR for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    args = parse_command_line()

    # generate SiLA2Server
    sila_server = SystemStatusProviderServer(cmd_args=args, simulation_mode=True)
