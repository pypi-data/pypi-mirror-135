# Local imports
from qwilfish.qwilfuzzer import QwilFuzzer
from qwilfish.constants import SIMPLE_GRAMMAR_EXAMPLE
from qwilfish.ethernet_frame import ETHERNET_FRAME_GRAMMAR
from qwilfish.socket_courier import SocketCourier
from qwilfish.logger import Logger
from qwilfish.session import start_session
from qwilfish.parser import parse_arguments
from qwilfish.service import start_service
from qwilfish.simple_client import start_simple_client
from qwilfish.grpc_oracle import GrpcOracle

def main():
    args = parse_arguments("normal")

    grammar = ETHERNET_FRAME_GRAMMAR
    fuzzer = QwilFuzzer(grammar, debug=args.debug)
    courier = SocketCourier(interface=args.interface)
    oracles = []
    if args.oracle == "grpc-oracle": # TODO plugin architecture for oracles
        oracles.append(GrpcOracle(args.grpc_address,
                                  args.grpc_port,
                                  args.worker,
                                  args.process_list))
    logger = Logger()
    if not args.log:
        logger.disable()

    return start_session(fuzzer, courier, oracles, logger, args.count)

def main_service():
    args = parse_arguments("service")

    return start_service(args.address, args.port)

def main_simple_client():
    args = parse_arguments("simple-client")

    return start_simple_client(args.message_type, args.address, args.port,
                               worker=args.worker,
                               process_list=args.process_list)
