from storage.mysql.mysql import MySQLStorage
from models.models import (
    CreateBetSQL,
)
from dataclasses import dataclass
from datetime import date

@dataclass
class ReadBet:
    league: str
    start_date: date
    end_date: date

@dataclass
class UpdateBet:
    league: str
    home_team: str
    away_team: str
    home_team_win_odds: float
    away_team_win_odds: float
    draw_odds: float
    game_date: date

@dataclass
class DeleteBet:
    league: str
    home_team: str
    away_team: str
    game_date: date

def test_create_user(db):
    test_cases = [
        {
        "name": "pass",
        "input": CreateBetSQL('epl', 'man u', 'arsenal', 2, 3,1, date(2023, 10, 10)
        ),
        "output": (201, 'Data stored successfully in MYSQL db')
        },
        {
        "name": "fail",
        "input": CreateBetSQL('epl', 'man u', 'arsenal', 2, 3,1, '2023-10-10'),
        "output": (500 ,"failed to store data:")
        }
    ]
    for test_case in test_cases:
        result = MySQLStorage(db).create_bet(test_case['input'])
        assert result == test_case['output']

def test_read_bet(db):
    test_cases = [
        {
        "name": "pass",
        "input": ReadBet('epl', date(2023, 10, 9), date(2023, 10, 12)),
        "output": (200, [{'home_team_win_odds': 2.0, 'game_date': '2023-10-10', 'home_team': 'man u', 'draw_odds': 1.0, 'away_team_win_odds': 3.0, 'league': 'epl', 'id': '1', 'away_team': 'arsenal'}], 'Data read from mysql db')
        },
        {
        "name": "fail",
        "input": ReadBet('seria', date(2023, 10, 9), date(2023, 10, 12)),
        "output": (403, None, 'Data not found')
        }
    ]

    for test_case in test_cases:
        MySQLStorage(db).create_bet(CreateBetSQL('epl', 'man u', 'arsenal', 2, 3,1, date(2023, 10, 10)))
        result = MySQLStorage(db).read_bet(test_case['input'])
        assert result[0] == test_case['output'][0]
        assert result[1] == test_case['output'][1]
        assert result[2] == test_case['output'][2]

def test_update_bet(db):
    test_cases = [
        {
        "name": "pass",
        "input": UpdateBet('epl', 'man u', 'arsenal', 1.3, 2.5, 3.8, date(2023, 10, 10)),
        "output": (200, 'Data updated in mysql db')
        },
        {
        "name": "fail",
        "input": UpdateBet('eplkk', 'man u', 'arsenal', 1.3, 2.5, 3.8, date(2023, 10, 10)),
        "output": (404, 'Data not available for updating')
        }
    ]
    for test_case in test_cases:
        MySQLStorage(db).create_bet(CreateBetSQL('epl', 'man u', 'arsenal', 2, 3,1, date(2023, 10, 10)))
        result = MySQLStorage(db).update_bet(test_case['input'])
        assert result[0] == test_case['output'][0]
        assert result[1] == test_case['output'][1]

def test_delete(db):
    test_cases = [
        {
        "name": "pass",
        "input": DeleteBet('epl', 'man u', 'arsenal', date(2023, 10, 10)),
        "output": (204, 'Data deleted from mysql db')
        },
        {
        "name": "fail",
        "input": DeleteBet('eplff', 'man u', 'arsenal', date(2023, 10, 10)),
        "output": (400, 'Data not found')
        }
    ]
    for test_case in test_cases:
        MySQLStorage(db).create_bet(CreateBetSQL('epl', 'man u', 'arsenal', 2, 3,1, date(2023, 10, 10)))
        result = MySQLStorage(db).delete_bet(test_case['input'])
        assert result == test_case['output']



