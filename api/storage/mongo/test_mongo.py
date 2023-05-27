from models.models import (
    CreateBetRequest,
    ReadBetRequest,
    UpdateBetRequest,
    DeleteBetRequest
)
from storage.mongo.mongo import MongoStorage

def test_create_bet(mongo_mock):
    test_cases = [
        {
            "name": "pass",
            "output": (201, 'Successfully created bet')
        }
    ]
    for test_case in test_cases:
        mong_storage = MongoStorage(mongo_mock, 'testdb', 'testcollection')
        result = mong_storage.create_bet(UpdateBetRequest(
            'epl', 'man u', 'arsenal', 0.35, 3, 2, '2023-10-10'
        ))
        assert result == test_case['output']


def test_read_bet(mongo_mock):
    test_cases = [
        {
            "name": "pass",
            "input": ReadBetRequest('upl', '2023-10-09', '2023-10-11'),
            "output": (200, [{'league': 'upl', 'home_team_win_odds': 0.35, 'away_team_win_odds': 3.0, 'game_date': '2023-10-10', 'away_team': 'arsenal', 'draw_odds': 2.0, 'home_team': 'man u'}])
        },
        {
        "name": "fail",
        "input": ReadBetRequest('NFL', '2022-10-09', '2022-10-11'),
        "output": (403,  None, "Data not found")
        }
    ]
    for test_case in test_cases:
        MongoStorage(mongo_mock, 'testdb', 'testcollection').create_bet(CreateBetRequest(
            'upl', 'man u', 'arsenal', 0.35, 3, 2, '2023-10-10'
        ))
        result = MongoStorage(mongo_mock, 'testdb', 'testcollection').read_bet(test_case['input'])
        assert result[0] == test_case['output'][0]
        assert result[1] == test_case['output'][1]

def test_update_bet(mongo_mock):
    test_cases = [
        {
            "name": "pass",
            "input": UpdateBetRequest('epl', 'man u', 'chelsea', 0.35, 3, 2, '2023-10-10'),
            "output": (200, 'Data updated successfully in mongodb')
        },
        {
        "name": "fail",
        "input": UpdateBetRequest('NFL', 'man u', 'chelsea', 2, 5, 4, '2025-10-10'),
        "output": (404, "Data with id  not available")
        }
    ]
    for test_case in test_cases:
        MongoStorage(mongo_mock, 'testdb', 'testcollection').create_bet(UpdateBetRequest(
            'epl', 'man u', 'chelsea', 2, 5, 4, '2025-10-10'
        ))
        result = MongoStorage(mongo_mock, 'testdb', 'testcollection').update_bet(test_case['input'])
        assert result[0] == test_case['output'][0]
        assert result[1] == test_case['output'][1]

def test_delete(mongo_mock):
    test_cases = [
        {
        "name": "pass",
        "input": DeleteBetRequest('epl', 'man u', 'chelsea', '2025-10-10'),
        "output": (204, 'Data deleted from mongodb')
        },
        {
        "name": "fail",
        "input": DeleteBetRequest('eplff', 'man u', 'chelsea', '2025-10-10'),
        "output": (400, 'Data not found')
        }
    ]
    for test_case in test_cases:
        MongoStorage(mongo_mock, 'testdb', 'testcollection').create_bet(UpdateBetRequest(
            'epl', 'man u', 'chelsea', 2, 5, 4, '2025-10-10'
        ))
        result = MongoStorage(mongo_mock, 'testdb', 'testcollection').delete_bet(test_case['input'])
        assert result[0] == test_case['output'][0]
        assert result[1] == test_case['output'][1]