import json
from models.models import (
    CreateBetRequest,
    ReadBetRequest,
    UpdateBetRequest,
    DeleteBetRequest
)

def test_create_bet(storage, helpers):
    test_cases = [
        {
            "name": "pass",
            "code_input": 201,
            "code_output": 201,
            "response": ""
        },
        {
            "name": "fail",
            "code_input": 400,
            "code_output": 400,
            "response": "Failed to store data in DB"
        }
    ]
    for test_case in test_cases:
        client = helpers.sport_bet_api(storage=storage)
        client.storage.create_bet.return_value = (test_case['code_input'], test_case['response'])
        output = client.create(CreateBetRequest('epl', 'man u', 'arsenal', 0.35, 3, 2, '2023-10-10' ))
        assert output.code == test_case['code_output']
        assert output.reason == test_case['response']


def test_read_api(storage, helpers):
    test_cases = [
        {
        "name": "pass",
        "code_input": 200,
        "code_output": 200,
        "response": json.dumps({'league': 'epl', 'home_team': 'man u', 'away_team': 'arsenal'}),
        "reason": ""
        },
        {
        "name": "fail",
        "code_input": 500,
        "code_output": 400,
        "response": " ",
        "reason": "Failed to read data from DB"
        }
    ]
    for test_case in test_cases:
        client = helpers.sport_bet_api(storage=storage)
        client.storage.read_bet.return_value = (test_case['code_input'],test_case['response'],  test_case['reason'])
        output = client.read(ReadBetRequest('epl', '2023-10-05', '2023-11-05'))
        assert output.code == test_case['code_output']

def test_update_bet(storage, helpers):
    test_cases = [
        {
        "name": "pass",
        "code_input": 200,
        "code_output": 200,
        "response": "successful"

        },
        {
        "name": "fail",
        "code_input": 500,
        "code_output": 400,
        "response": "Failed to update data in DB"
        }
    ]
    for test_case in test_cases:
        client = helpers.sport_bet_api(storage=storage)
        client.storage.update_bet.return_value = (test_case['code_input'], test_case['response'])
        output = client.update(UpdateBetRequest(
            'seria a', 'man u', 'arsenal', 1, 2.3, 0.5, '2023-06-10'
        ))
        assert output.code == test_case['code_output']
        assert output.reason == test_case["response"]

def test_delete(storage, helpers):
    test_cases = [
        {
        "name": "pass",
        "code_input": 204,
        "code_output": 204,
        "response": "deleted successfully"
        },
        {
        "name": "fail",
        "code_input": 500,
        "code_output": 400,
        "response": "Failed to delete data from DB"
        }
    ]
    for test_case in test_cases:
        client = helpers.sport_bet_api(storage=storage)
        client.storage.delete_bet.return_value = (test_case['code_input'], test_case['response'])
        output = client.delete(DeleteBetRequest(
            'epl', 'man u', 'arsenal', '2023-10-10'
        ))
        assert output.code == test_case['code_output']
        assert output.reason == test_case['response']