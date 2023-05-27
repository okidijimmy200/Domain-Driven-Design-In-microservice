import grpc
from concurrent import futures
import generated.sportbet_pb2 as sportbet_pb2
import generated.sportbet_pb2_grpc as sportbet_pb2_grpc
from service.interfaces import SportsBettingInterface
from models.models import (
    CreateBetRequest,
    ReadBetRequest,
    UpdateBetRequest,
    DeleteBetRequest
)

class SportBetManagementService(sportbet_pb2_grpc.SportBetManagementServiceServicer):
    sports_service: SportsBettingInterface
    def __init__(self, sports_service: SportsBettingInterface) -> None:
        self.sports_service = sports_service

    def CreateBet(self, request, context):
        response = self.sports_service.create(CreateBetRequest(
            request.league, 
            request.home_team, 
            request.away_team, 
            request.home_team_win_odds, 
            request.away_team_win_odds, 
            request.draw_odds, 
            request.game_date
        ))
        return sportbet_pb2.CreateBetResponse(code=response.code, reason= response.reason)

    def ReadBet(self, request, context):
        response = self.sports_service.read(ReadBetRequest(
            request.league,
            request.start_date,
            request.end_date
        ))
        return sportbet_pb2.ReadBetResponse(code=response.code, response=response.response, reason=response.reason)

    def UpdateBet(self, request, context):
        response = self.sports_service.update(UpdateBetRequest(
            request.league, 
            request.home_team, 
            request.away_team, 
            request.home_team_win_odds, 
            request.away_team_win_odds, 
            request.draw_odds, 
            request.game_date
        ))
        return sportbet_pb2.UpdateBetResponse(code=response.code, reason= response.reason)

    def DeleteBet(self, request, context):
        response = self.sports_service.delete(DeleteBetRequest(
            request.league, 
            request.home_team, 
            request.away_team,  
            request.game_date
        ))
        return sportbet_pb2.DeleteBetResponse(code=response.code, reason= response.reason)

def run (
    sports_service: SportsBettingInterface
):
    server =  grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sportbet_pb2_grpc.add_SportBetManagementServiceServicer_to_server(
        SportBetManagementService(sports_service), server
    )
    print("server started")
    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()