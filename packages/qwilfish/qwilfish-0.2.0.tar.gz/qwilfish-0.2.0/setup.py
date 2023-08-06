from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

def generate_grpc():
    print("Generating grpc code...")
    import grpc_tools.protoc

    grpc_tools.protoc.main([
        "grpc_tools.protoc",
        "--proto_path=proto/",
        "--python_out=src/qwilfish/generated",
        "--grpc_python_out=src/qwilfish/generated",
        "feedback_interface.proto"
    ])

class BuildPyWithGrpcGeneration(build_py):
    def run(self):
        generate_grpc()
        super(BuildPyWithGrpcGeneration, self).run()

class DevelopWithGrpcGeneration(develop):
    def run(self):
        generate_grpc()
        super(DevelopWithGrpcGeneration, self).run()

setup(cmdclass={"build_py": BuildPyWithGrpcGeneration,
                "develop": DevelopWithGrpcGeneration})
