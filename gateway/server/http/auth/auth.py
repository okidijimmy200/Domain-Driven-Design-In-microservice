from flask import request
from flask import Blueprint, jsonify
from models.user_models import LoginRequest
import server.http.server as server

auth_api = Blueprint("auth", __name__)


@auth_api.route("/login", methods=["POST"])
def login():
    try:
        data: dict = request.get_json()
        req = LoginRequest(data.get("email"), data.get("password"))
        response = server.auth_service.login(req)

        reason = {
            "code": response.code,
            "reason": response.reason,
            "token": response.token,
        }
        print(reason)
        return jsonify(reason)
    except Exception as e:
        result = f"-Error " + f"{type(e).__name__} {str(e)}"
        print(result)
        return result
