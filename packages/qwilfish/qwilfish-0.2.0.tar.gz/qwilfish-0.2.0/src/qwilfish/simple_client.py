# Third-party imports
import grpc

# Local imports
from qwilfish.generated.feedback_interface_pb2 import (
    FeedbackDataRequest, FeedbackDataResponse, ProcessFeedbackData,
    TerminateRequest, TerminateResponse
)
from qwilfish.generated.feedback_interface_pb2_grpc import (
    FeedbackInterfaceStub
)

def start_simple_client(message_type, address, port, **kwargs):
    with grpc.insecure_channel(address + ":" + str(port)) as channel:
        stub = FeedbackInterfaceStub(channel)

        if message_type == "request":
            request = FeedbackDataRequest()

            worker = kwargs.get("worker")
            if worker:
                request.standalone_worker = worker

            process_list = kwargs.get("process_list")
            if process_list:
                request.process_list.extend(process_list)

            process_data = stub.GetFeedbackData(request=request)
        elif message_type == "terminate":
            process_data = stub.Terminate(TerminateRequest())
        else: # Should not happen if argparse does its job right
            raise ValueError("Unrecognized message type '" + message_type + \
                             "' for qwilfish gRPC feedback interface!")

    print(process_data)
