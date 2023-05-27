from flask import request
from flask import Blueprint, jsonify
import server.http.server as server
from models.user_models import SignUpRequest

registration_api = Blueprint("registration_api", __name__)


@registration_api.route("/signup", methods=["POST"])
def signup():
    try:
        data: dict = request.get_json()
        req = SignUpRequest(
            data.get("username"), data.get("email"), data.get("password")
        )
        response = server.reg_service.signup(req)

        reason = {"code": response.code, "reason": response.reason}
        print(response)
        return jsonify(reason)
    except Exception as e:
        result = f"-Error " + f"{type(e).__name__} {str(e)}"
        print(result)
        return result
