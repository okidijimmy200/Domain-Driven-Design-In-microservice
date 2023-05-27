import os
from flask import Flask
from service.interface import AuthProvider, RegistrationProvider, SportbetProvider
from server.http.auth.auth import auth_api
from server.http.register.register import registration_api
from server.http.middleware.middleware import TokenRequired

# services
auth_service: AuthProvider
reg_service: RegistrationProvider
sport_service: SportbetProvider

# middleware
token_middleware: TokenRequired


def get_app(auth: AuthProvider, reg: RegistrationProvider, sport: SportbetProvider):
    app = Flask(__name__)

    global auth_service, reg_service, sport_service, token_middleware
    auth_service = auth
    reg_service = reg
    sport_service = sport
    token_middleware = TokenRequired(auth_service)

    import server.http.api.api as sport_bet

    app.register_blueprint(auth_api, name="auth")
    app.register_blueprint(registration_api, name="register")
    app.register_blueprint(sport_bet.sport_bet, name="api")

    return app
