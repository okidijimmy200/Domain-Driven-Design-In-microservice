import grpc, os
import generated.auth_pb2 as auth_pb2
import generated.auth_pb2_grpc as auth_pb2_grpc


class Auth:
    def __init__(self) -> None:
        self.host = os.environ.get("AUTH_SERVICE_HOST")
        self.server_port = os.environ.get("AUTH_SERVICE_PORT")

        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")
        self.stub = auth_pb2_grpc.UserManagenmentServiceStub(self.channel)

    def login(self, req):
        login_request = auth_pb2.LoginRequest(email=req.email, password=req.password)
        return self.stub.Login(login_request)

    def validate_token(self, token):
        token_required = auth_pb2.ValidateTokenRequest(token=token)
        return self.stub.ValidateToken(token_required)
