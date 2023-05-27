from flask import jsonify, request
from functools import wraps
from service.interface import AuthProvider


"""decorator for verifying jwt"""


class TokenRequired:
    def __init__(self, auth_service: AuthProvider) -> None:
        self.auth_service = auth_service

    """decorator for verifying jwt"""

    def validate_token(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # jwt is passed in the request
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401

            """decode the payload to get stored details"""
            try:
                # result = get_token.get_current_user_token(f, token, *args, **kwargs)
                response = self.auth_service.validate_token(token)
                # if type(response.user_id)

                if response.code != 200:
                    return {
                        "message": response.reason,
                        "data": None,
                        "error": "Unauthorized",
                    }, response.code

                reason = jsonify(
                    {
                        "code": response.code,
                        "reason": response.reason,
                        "user_id": response.user_id,
                    }
                )
                return f(reason, *args, **kwargs)
            except Exception as e:
                result = f"-Error " + f"{type(e).__name__} {str(e)}"
                print(result)
                return result

        return decorated
