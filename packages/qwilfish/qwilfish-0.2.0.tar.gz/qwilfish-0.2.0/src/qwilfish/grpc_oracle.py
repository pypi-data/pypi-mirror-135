# Third-party imports
import grpc

# Local imports
from qwilfish.generated.feedback_interface_pb2 import (
    FeedbackDataRequest, FeedbackDataResponse, ProcessFeedbackData
)
from qwilfish.generated.feedback_interface_pb2_grpc import (
    FeedbackInterfaceStub
)

class GrpcOracle:
    def __init__(self, address="127.0.0.1", port=54545, worker=None,
                 process_list=None):
        self.address = address
        self.port = port
        self.worker = worker
        self.process_list = process_list

    def report(self):
        msg = ""

        with grpc.insecure_channel(self.address + ":" +
                                   str(self.port)) as channel:
            stub = FeedbackInterfaceStub(channel)

            request = FeedbackDataRequest()

            if self.worker:
                request.standalone_worker = self.worker

            if self.process_list:
                request.process_list.extend(self.process_list)

            process_data = stub.GetFeedbackData(request=request)

            msg = "gRPC Oracle report:\n" + repr(process_data)

        return msg
