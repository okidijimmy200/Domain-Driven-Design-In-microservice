import grpc, os
import generated.sportbet_pb2 as sportbet_pb2
import generated.sportbet_pb2_grpc as sportbet_pb2_grpc


class SportsBet:
    def __init__(self) -> None:
        self.host = os.environ.get("BET_SERVICE_HOST")
        self.server_port = os.environ.get("BET_SERVICE_PORT")

        self.channel = grpc.insecure_channel(f"{self.host}: {self.server_port}")
        self.stub = sportbet_pb2_grpc.SportBetManagementServiceStub(self.channel)

    def create_bet(self, req):
        bet_request = sportbet_pb2.CreateBetRequest(
            league=req.league,
            home_team=req.home_team,
            away_team=req.away_team,
            home_team_win_odds=req.home_team_win_odds,
            away_team_win_odds=req.away_team_win_odds,
            draw_odds=req.draw_odds,
            game_date=req.game_date,
        )
        return self.stub.CreateBet(bet_request)

    def read_bet(self, req):
        read_request = sportbet_pb2.ReadBetRequest(
            league=req.league, start_date=req.start_date, end_date=req.end_date
        )
        return self.stub.ReadBet(read_request)

    def update_bet(self, req):
        update_request = sportbet_pb2.UpdateBetRequest(
            league=req.league,
            home_team=req.home_team,
            away_team=req.away_team,
            home_team_win_odds=req.home_team_win_odds,
            away_team_win_odds=req.away_team_win_odds,
            draw_odds=req.draw_odds,
            game_date=req.game_date,
        )
        return self.stub.UpdateBet(update_request)

    def delete_bet(self, req):
        delete_request = sportbet_pb2.DeleteBetRequest(
            league=req.league,
            home_team=req.home_team,
            away_team=req.away_team,
            game_date=req.game_date,
        )
        return self.stub.DeleteBet(delete_request)
