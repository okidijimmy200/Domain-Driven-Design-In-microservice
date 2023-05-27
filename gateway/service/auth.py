import json
from service.interface import AuthProvider
from models.user_models import (
    LoginRequest,
    ValidateTokenRequest,
    ValidateTokenResponse,
    LoginResponse,
    validate
)


class AuthService:
    auth_provider: AuthProvider

    def __init__(self, auth_provider: AuthProvider):
        self.auth_provider = auth_provider

    def login(self, request: LoginRequest) -> LoginResponse:
        try:
            valid, reason = LoginRequest.validate(request)
            if not valid:
                return LoginResponse(400, reason)
            """login user"""
            return self.auth_provider.login(request)
        except:
            return LoginResponse(500, reason)

    def validate_token(self, request: ValidateTokenRequest) -> ValidateTokenResponse:
        try:
            valid, reason = validate(request)
            if not valid:
                return ValidateTokenResponse(400, reason, "")

            """validate user token"""
            return self.auth_provider.validate_token(request)
        except:
            return ValidateTokenResponse(500, "Invalid token request", "")
