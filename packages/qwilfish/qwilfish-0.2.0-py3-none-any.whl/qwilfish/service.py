# Standard library imports
from concurrent import futures
import threading
import importlib.util
import sys
import os.path
import re

# Third-party imports
import grpc

# Local imports
from qwilfish.generated.feedback_interface_pb2 import (
    FeedbackDataResponse, ProcessFeedbackData,
    TerminateResponse
)
from qwilfish.generated.feedback_interface_pb2_grpc import (
    FeedbackInterfaceServicer, add_FeedbackInterfaceServicer_to_server
)

class QwilfishGrpcServicer(FeedbackInterfaceServicer):

    DEFAULT_STANDALONE_FUNC_NAME = "run"

    def __init__(self, terminate_event):
        self.terminate_event = terminate_event

    def GetFeedbackData(self, request, context):
        '''Dummy implementation, replace with your own code'''
        if request.standalone_worker: # Execute user-specified module
            response = self.handle_request_standalone(request, context)
        else: # Execute implementation native to this package
            response = self.handle_request(request, context)

        return response

    def Terminate(self, request, context):
        self.terminate_event.set()
        return TerminateResponse()

    def handle_request_standalone(self, request, context):
        worker = request.standalone_worker.split(":")
        if len(worker) >= 2:
            file_path = worker[0]
            func_name = worker[1]
        elif len(worker) == 1:
            file_path = worker[0]
            func_name = QwilfishGrpcServicer.DEFAULT_STANDALONE_FUNC_NAME
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name,
                                                      file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        if not hasattr(module, func_name):
            raise AttributeError("Module '" + module_name +
                                 "' has no attribute '" + func_name + "'")

        func = getattr(module, func_name)

        if not callable(func):
            raise AttributeError("Attribute '" + func_name + "' in module '" +
                                 module_name + "' is not callable")

        retval = func(request.process_list)

        if not isinstance(retval, dict):
            raise AttributeError("'" + func_name + "' in module '" +
                                 module_name + "did not return a dict")

        data = []
        for key, val in retval.items():
            data.append(ProcessFeedbackData(process_name=key,
                                            cpu_usage=val[0],
                                            mem_usage=val[1]))

        return FeedbackDataResponse(data=data)

    def handle_request(self, request, context):
        """Dummy implementation. Replace with your own code."""
        data1 = ProcessFeedbackData(process_name="proc1",
                                    cpu_usage=0,
                                    mem_usage=1)
        data2 = ProcessFeedbackData(process_name="proc2",
                                    cpu_usage=42,
                                    mem_usage=1337)
        response = FeedbackDataResponse(data=[data1, data2])

        return response

def start_service(address, port):
    # Create objects for termination event and gRPC server
    terminate_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Create the qwilfish servicer and add it to the gRPC server
    add_FeedbackInterfaceServicer_to_server(
        QwilfishGrpcServicer(terminate_event), server)

    # Start the server
    server.add_insecure_port(address + ":" + str(port))
    server.start()
    print("Service started on port " + str(port) + "!")

    # Block this thread until a handler signals to terminate
    terminate_event.wait()
    print("Shutting down service on port " + str(port) + "...")

    # 1 second grace time then goodbye
    server.stop(1)
    print("Bye!")

    return 0
