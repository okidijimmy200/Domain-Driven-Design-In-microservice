from server.http.server import get_app
from provider.auth.auth import Auth
from provider.register.register import Register
from provider.api.api import SportsBet
from service.auth import AuthService
from service.registration import RegistrationService
from service.api import SportBetService


if __name__ == "__main__":
    app = get_app(
        AuthService(Auth()),
        RegistrationService(Register()),
        SportBetService(SportsBet()),
    )
    app.run(host="localhost", port=8000, debug=True)
