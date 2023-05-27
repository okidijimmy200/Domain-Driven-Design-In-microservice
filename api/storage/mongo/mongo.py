import datetime
from typing import Tuple
from bson.objectid import ObjectId
from service.interfaces import StorageInterface
from pymongo import MongoClient
from models.models import (
    SportBet, 
    ReadBetRequest, 
    ReadBetResponse, 
    UpdateBetRequest, 
    UpdateBetResponse,
    DeleteBetRequest,
    DeleteBetResponse
)
from storage.mysql.models import BettingSchema

class MongoStorage(StorageInterface):
    def __init__(self, mongo_conn, database, collection) -> None:
        self.client = mongo_conn

        cursor = self.client[database]
        self.collection = cursor[collection]

    def create_bet(self, bet: SportBet) -> Tuple[int, str]:
        try:
            '''create a new bet'''
            x = bet.game_date
            y = x.split(' ')
            z = y[0]
            new_take = z.split('-')

            new_data = {
                    "league": f"{bet.league}", 
                    "home_team": f"{bet.home_team}",
                    "away_team":  f"{bet.away_team}",
                    "home_team_win_odds":  f"{bet.home_team_win_odds}",
                    "away_team_win_odds":  f"{bet.away_team_win_odds}",
                    "draw_odds":  f"{bet.draw_odds}",
                    "game_date":  datetime.datetime(int(new_take[0]), int(new_take[1]), int(new_take[2]))
                }
            self.collection.insert_one(new_data)

            return 201, f'Successfully created bet'
        except Exception as e:
            reason = (
                f"failed to create bet in smongodb: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None

    def read_bet(self, data: ReadBetRequest) -> ReadBetResponse:
        try:
            '''read data from mongodb'''
            schema = BettingSchema()

            end_date = data.end_date.split('-')
            start_date = data.start_date.split('-')

            '''query the db'''
            query = self.collection.find({
                'league': f"{data.league}",
                'game_date': {'$lte': datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]), 0, 0), '$gte': datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]), 0, 0) }
            }, {'_id': 0})

            
            lst = []
            for doc in query:
                lst.append(doc)

            reason = schema.dump(lst, many=True)
            print(reason)
            if len(reason) == 0:
                return 403, None, 'Data not found'
            return 200, reason, 'Data read from mongodb'
        except Exception as e:
            reason = (
                f"failed to read data from storage: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None

    def update_bet(self, data: UpdateBetRequest) -> UpdateBetResponse:
        try:
            x = data.game_date
            y = x.split(' ')
            z = y[0]
            new_take = z.split('-')

            schema = BettingSchema()

            new_data = {
                    "league": f"{data.league}", 
                    "home_team": f"{data.home_team}",
                    "away_team":  f"{data.away_team}",
                    "home_team_win_odds":  f"{data.home_team_win_odds}",
                    "away_team_win_odds":  f"{data.away_team_win_odds}",
                    "draw_odds":  f"{data.draw_odds}",
                    "game_date":  datetime.datetime(int(new_take[0]), int(new_take[1]), int(new_take[2]))
                }
            data_query = {
                    "league": f"{data.league}", 
                    "home_team": f"{data.home_team}",                                      
                    "away_team":  f"{data.away_team}"
            }

            query = self.collection.find(data_query)
            lst = []
            for doc in query:
                lst.append(doc)  
            print(lst)

            reason = schema.dump(lst, many=True)          

            print(reason)
            if len(reason) == 0:
                return 404, f'Data with id  not available'
            
            self.collection.update_one(
                {'_id': lst[0]['_id']},
                {"$set": new_data}
            )
            return 200, 'Data updated successfully in mongodb'

        except Exception as e:
            reason = (
                f"failed to update data in mongodb: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None

    def delete_bet(self, data: DeleteBetRequest) -> DeleteBetResponse:
        try:
            x = data.game_date
            y = x.split(' ')
            z = y[0]
            new_take = z.split('-')

            new_data = {
                'league': f"{data.league}",
                'home_team': f'{data.home_team}',
                'away_team': f'{data.away_team}',
                'game_date': datetime.datetime(int(new_take[0]), int(new_take[1]), int(new_take[2]))
                
            }

            query = self.collection.find(new_data, {'_id': 0})
            lst = []
            for doc in query:
                lst.append(doc)
            print('if test')
            print(lst)
            
            if len(lst) == 0:
                return 400, 'Data not found'
            self.collection.delete_one(new_data)
            return 204, 'Data deleted from mongodb'
        except Exception as e:
            reason = (
                f"failed to delete data from mongodb: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None