from abc import ABC, abstractmethod
from models.models import  SportBet, CreateBetRequest, CreateBetResponse, ReadBetRequest, ReadBetResponse, UpdateBetRequest, UpdateBetResponse, DeleteBetRequest, DeleteBetResponse
from typing import Tuple

class SportsBettingInterface(ABC):
    @abstractmethod
    def create(self, data: CreateBetRequest) -> CreateBetResponse:
        pass

    @abstractmethod
    def read(self, data: ReadBetRequest) -> ReadBetResponse:
        pass

    @abstractmethod
    def update(self, data: UpdateBetRequest) -> UpdateBetResponse:
        pass

    @abstractmethod
    def delete(self, data: DeleteBetRequest) -> DeleteBetResponse:
        pass

class StorageInterface(ABC):
    @abstractmethod
    def create_bet(self, bet: SportBet) -> Tuple[int, str]:
        pass

    @abstractmethod
    def read_bet(self, data: ReadBetRequest) -> ReadBetResponse:
        pass

    @abstractmethod
    def update_bet(self, data: UpdateBetRequest) -> UpdateBetResponse:
        pass

    @abstractmethod
    def delete_bet(self, data: DeleteBetRequest) -> DeleteBetResponse:
        pass