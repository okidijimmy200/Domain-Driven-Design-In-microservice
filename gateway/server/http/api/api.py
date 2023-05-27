from flask import request
from flask import Blueprint, jsonify
from google.protobuf.json_format import MessageToJson
from models.sportbet_models import (
    CreateBetRequest,
    UpdateBetRequest,
    ReadBetRequest,
    DeleteBetRequest,
)
import server.http.server as server


sport_bet = Blueprint("sport_bet", __name__)


@sport_bet.route("/createbet", methods=["POST"])
@server.token_middleware.validate_token
def create_bet(current_user):
    try:
        if current_user:
            print(current_user.data)
            data: dict = request.get_json()
            # there needs to be isolation of provider from server from everthing
            # except service. (the provider only imports models and service)

            req = CreateBetRequest(
                data.get("league"),
                data.get("home_team"),
                data.get("away_team"),
                data.get("home_team_win_odds"),
                data.get("away_team_win_odds"),
                data.get("draw_odds"),
                data.get("game_date"),
            )

            response = server.sport_service.create_bet(req)

            if response.code == 500:
                raise Exception(response.reason)

            # return jsonify(MessageToJson(response)), response.code # get unstructured response, response.code not working bse of int
            return MessageToJson(response)

    except Exception as e:
        result = f"-Error " + f"{type(e).__name__} {str(e)}"
        print(result)
        return jsonify({"code": 500, "reason": "Server error occured"})


@sport_bet.route("/readbet", methods=["GET"])
@server.token_middleware.validate_token
def read_bet(current_user):
    try:
        if current_user:
            data: dict = request.args.to_dict()
            req = ReadBetRequest(
                data.get("league"), data.get("start_date"), data.get("end_date")
            )
            response = server.sport_service.read_bet(req)
            # return jsonify({

            # })
            return MessageToJson(response)
    except Exception as e:
        result = f"-Error " + f"{type(e).__name__} {str(e)}"
        print(result)
        return result


@sport_bet.route("/updatebet", methods=["PUT"])
@server.token_middleware.validate_token
def update_bet(current_user):
    try:
        if current_user:
            data: dict = request.args.to_dict()
            req = UpdateBetRequest(
                data.get("league"),
                data.get("home_team"),
                data.get("away_team"),
                float(data.get("home_team_win_odds")),
                float(data.get("away_team_win_odds")),
                float(data.get("draw_odds")),
                data.get("game_date"),
            )
            response = server.sport_service.update_bet(req)
            reason = {"code": response.code, "reason": response.reason}
            # print(response)
            return jsonify(reason)

    except Exception as e:
        result = f"-Error " + f"{type(e).__name__} {str(e)}"
        print(result)
        return result


@sport_bet.route("/deletebet", methods=["DELETE"])
@server.token_middleware.validate_token
def delete(current_user):
    try:
        if current_user:
            data: dict = request.args.to_dict()
            req = DeleteBetRequest(
                data.get("league"),
                data.get("home_team"),
                data.get("away_team"),
                data.get("game_date"),
            )
            response = server.sport_service.delete_bet(req)
            reason = {"code": response.code, "reason": response.reason}
            # print(response)
            return jsonify(reason)
    except Exception as e:
        result = f"-Error " + f"{type(e).__name__} {str(e)}"
        print(result)
        return result
