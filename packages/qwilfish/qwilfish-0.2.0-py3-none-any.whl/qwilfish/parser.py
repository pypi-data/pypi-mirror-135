# Standard library imports
import argparse

DEFAULT_GRPC_ADDRESS = "127.0.0.1"
DEFAULT_GRPC_PORT = 54545

def parse_arguments(mode="normal"):
    if mode == "normal": # user@computer $ qwilfish
        add_mode_specific_args = add_normal_mode_args
        epilog = "See 'qwilfish-service' for a sample of a gRPC oracle service"
    elif mode == "service": # user@computer $ qwilfish-service
        add_mode_specific_args = add_service_mode_args
        epilog = None
    elif mode == "simple-client": # user@computer $ qwilfish-simple-client
        add_mode_specific_args = add_simple_client_mode_args
        epilog = None
    else:
        raise ValueError("mode: " + str(mode) + "unrecognized by qwilfish")

    parser = argparse.ArgumentParser(epilog=epilog)

    parser.add_argument("-l", "--log",
                        dest="log",
                        help="keep a log file",
                        action="store_true")

    parser.add_argument("-d", "--debug",
                        dest="debug",
                        help="enable debug output",
                        action="store_true")

    add_mode_specific_args(parser)

    return parser.parse_args()

def add_normal_mode_args(parser):
    parser.add_argument("-i", "--interface",
                        dest="interface",
                        help="network interface to transmit fuzzed packets on",
                        default="lo")

    parser.add_argument("-c", "--count",
                        dest="count",
                        help="number of fuzzed packets to transmit",
                        type=int,
                        default=1)

    subparsers = parser.add_subparsers(help="enable oracle",
                                      dest="oracle")

    g_parser = subparsers.add_parser("grpc-oracle",
                                     help="enable gRPC oracle")

    g_parser.add_argument("-a", "--address",
                          dest="grpc_address",
                          help="gRPC servicer address",
                          default=DEFAULT_GRPC_ADDRESS)

    g_parser.add_argument("-p", "--port",
                          dest="grpc_port",
                          help="gRPC servicer port",
                          default=DEFAULT_GRPC_PORT)

    g_parser.add_argument("-s", "--standalone-worker",
                          dest="worker",
                          type=str,
                          help="invoke '/path/to/file.py:some_func' to do \
                                the work for the gRPC servicer")

    g_parser.add_argument("process_list",
                          nargs="+",
                          type=str,
                          help="processes to get feedback from")

def add_service_mode_args(parser):
    parser.add_argument("-a", "--address",
                        dest="address",
                        help="incoming addresses to accept",
                        default="0.0.0.0")

    parser.add_argument("-p", "--port",
                        dest="port",
                        help="service port to listen to",
                        type=int,
                        default=DEFAULT_GRPC_PORT)

def add_simple_client_mode_args(parser):
    parser.add_argument("-a", "--address",
                        dest="address",
                        help="address of the target server",
                        default=DEFAULT_GRPC_ADDRESS)

    parser.add_argument("-p", "--port",
                        dest="port",
                        help="port of the target server",
                        type=int,
                        default=DEFAULT_GRPC_PORT)

    parser.set_defaults(worker=None, process_list=None)

    subparsers = parser.add_subparsers(help="type of message to send",
                                       dest="message_type",
                                       required=True)

    r_parser = subparsers.add_parser("request",
                                     help="send a request message")

    r_parser.add_argument("-s", "--standalone-worker",
                          dest="worker",
                          type=str,
                          help="invoke 'run' function defined in its own file")

    r_parser.add_argument("process_list",
                          nargs="+",
                          type=str,
                          help="processes to get feedback from")

    t_parser = subparsers.add_parser("terminate",
                                     help="send a terminate message")
