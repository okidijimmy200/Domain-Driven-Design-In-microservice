from typing import Tuple
from sqlalchemy.orm import sessionmaker
from service.interfaces import StorageInterface
from storage.mysql.models import BettingModel, BettingSchema
from models.models import (
    SportBet, 
    ReadBetRequest, 
    ReadBetResponse, 
    UpdateBetRequest, 
    UpdateBetResponse,
    DeleteBetRequest,
    DeleteBetResponse
)

class MySQLStorage(StorageInterface):
    db: sessionmaker
    def __init__(self, db: sessionmaker) -> None:
        self.db = db

    def create_bet(self, bet: SportBet) -> Tuple[int, str]:
        try:
            new_data = BettingModel(
                league=bet.league,
                home_team=bet.home_team,
                away_team=bet.away_team,
                home_team_win_odds=bet.home_team_win_odds,
                away_team_win_odds=bet.away_team_win_odds,
                draw_odds=bet.draw_odds,
                game_date=bet.game_date
            )
            self.db.add(new_data)
            self.db.commit()
            result = 'Data stored successfully in MYSQL db'
            return 201, result
        except Exception as e:
            reason = (
                f"failed to store data: "
                + f"{type(e).__name__} {str(e)}"
            )
            result = 'failed to store data:'
            print(reason) # TODO: make log
            return 500, result

    def read_bet(self, data: ReadBetRequest) -> ReadBetResponse:
        try:
            schema = BettingSchema()
            q = self.db.query(BettingModel).filter(BettingModel.league == data.league, BettingModel.game_date.between(data.start_date, data.end_date)).first()
            reason = schema.dump([q], many=True)
            if len(reason[0]) == 0:
                return 403, None, 'Data not found'
            return 200, reason, 'Data read from mysql db'
        except Exception as e:
            reason = (
                f"failed to read data from storage: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None

    def update_bet(self, data: UpdateBetRequest) -> UpdateBetResponse:
        try:
            q = self.db.query(BettingModel).filter(
                BettingModel.league == data.league, 
                BettingModel.home_team == data.home_team,
                BettingModel.away_team == data.away_team
                ).update({
                    BettingModel.league : data.league,
                    BettingModel.home_team : data.home_team,
                    BettingModel.away_team :data.away_team,
                    BettingModel.home_team_win_odds :data.home_team_win_odds,
                    BettingModel.away_team_win_odds :data.away_team_win_odds,
                    BettingModel.draw_odds : data.draw_odds,
                    BettingModel.game_date : data.game_date
                })
            self.db.commit()
            print(q)
            
            if q == 0:
                return 404, f'Data not available for updating'
            
            return 200, 'Data updated in mysql db'
        except Exception as e:
            result = (
                f"-Failed to update data in MYSQL DB, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            reason = '-Failed to update data in db'
            return 500, reason
    
    def delete_bet(self, data: DeleteBetRequest) -> DeleteBetResponse:
        try:
            q = self.db.query(BettingModel).filter(
                BettingModel.league == data.league,
                BettingModel.home_team == data.home_team,
                BettingModel.home_team == data.home_team,
                BettingModel.home_team == data.home_team,
                BettingModel.away_team == data.away_team,
                BettingModel.game_date == data.game_date).delete()
            self.db.commit()
            if q == 0:
                return 400, 'Data not found'
            return 204, 'Data deleted from mysql db'
        except Exception as e:
            reason = (
                f"failed to delete data from storage: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None