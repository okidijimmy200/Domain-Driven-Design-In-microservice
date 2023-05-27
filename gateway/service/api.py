from service.interface import SportbetProvider
from models.sportbet_models import (
    CreateBetRequest,
    CreateBetResponse,
    ReadBetRequest,
    ReadBetResponse,
    UpdateBetRequest,
    UpdateBetResponse,
    DeleteBetRequest,
    DeleteBetResponse,
)


class SportBetService:
    sport_provider = SportbetProvider

    def __init__(self, sport_provider: SportbetProvider) -> None:
        self.sport_provider = sport_provider

    def create_bet(self, req: CreateBetRequest) -> CreateBetResponse:
        """create bet"""
        return self.sport_provider.create_bet(req)

    def read_bet(self, req: ReadBetRequest) -> ReadBetResponse:
        """query and read bet"""
        return self.sport_provider.read_bet(req)

    def update_bet(self, req: UpdateBetRequest) -> UpdateBetResponse:
        """update bet"""
        return self.sport_provider.update_bet(req)

    def delete_bet(self, req: DeleteBetRequest) -> DeleteBetResponse:
        """delete bet"""
        return self.sport_provider.delete_bet(req)
