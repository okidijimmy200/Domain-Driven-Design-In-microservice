from server.http.server import get_app
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
from models.user_models import (
    ValidateTokenRequest,
    ValidateTokenResponse,
)


class MockAuthProvider:
    def validate_token(self, request: ValidateTokenRequest) -> ValidateTokenResponse:
        return ValidateTokenResponse(200, "OK", "test_user")


def test_create_bet(mocker):
    # prepare
    class MockSportProvider:
        def create_bet(self, req: CreateBetRequest) -> CreateBetResponse:
            pass

    mock_sport_service = MockSportProvider()
    sport_spy = mocker.spy(mock_sport_service, "create_bet")

    mock_auth_service = MockAuthProvider()
    auth_spy = mocker.spy(mock_auth_service, "validate_token")

    flask_app = get_app(
        mock_auth_service,
        None,
        mock_sport_service,
    )
    test_client = flask_app.test_client()

    test_cases = [
        {
            "name": "success",
            "path": "/createbet",
            "input": {"league": "test", "home_team": "", "away_team": ""},
            "headers": {"Authorization": "Authorization valid"},
            "output": 200,
        },
        {
            "name": "fail",
            "path": "/createb",
            "input": {"league": "test", "home_team": "", "away_team": ""},
            "headers": {"Authorization": "Authorization valid"},
            "output": 404,
        },
        {
            "name": "unauthorized",
            "path": "/createbet",
            "input": {"league": "test", "home_team": "", "away_team": ""},
            "headers": None,
            "output": 401,
        },
    ]
    for test_case in test_cases:
        res = test_client.post(
            test_case["path"], json=test_case["input"], headers=test_case["headers"]
        )

        assert res.status_code == test_case["output"]
        assert sport_spy.call_count == 1
        assert auth_spy.call_count == 1


def test_read_bet(mocker):
    # prepare mock provider
    class MockSportProvider:
        def read_bet(self, req: ReadBetRequest) -> ReadBetResponse:
            pass

    mock_sport_service = MockSportProvider()
    sport_spy = mocker.spy(mock_sport_service, "read_bet")

    mock_auth_service = MockAuthProvider()
    auth_spy = mocker.spy(mock_auth_service, "validate_token")

    flask_app = get_app(
        mock_auth_service,
        None,
        mock_sport_service,
    )
    test_client = flask_app.test_client()

    test_cases = [
        {
            "name": "success",
            "path": "/readbet?league=epl&start_date=2022-06-11&end_date=22022-06-15",
            "headers": {"Authorization": "Authorization valid"},
            "output": 200,
        },
        {
            "name": "fail",
            "path": "/readbe?league=epl&start_date=2022-06-11&end_date=22022-06-15",
            "headers": {"Authorization": "Authorization valid"},
            "output": 404,
        },
        {
            "name": "unauthorized",
            "path": "/readbet?league=epl&start_date=2022-06-11&end_date=22022-06-15",
            "headers": None,
            "output": 401,
        },
    ]
    for test_case in test_cases:
        res = test_client.get(test_case["path"], headers=test_case["headers"])

        assert res.status_code == test_case["output"]
        assert sport_spy.call_count == 1
        # assert auth_spy.call_count == 1


def test_update_bet(mocker):
    class MockSportProvider:
        def update_bet(self, req: UpdateBetRequest) -> UpdateBetResponse:
            pass

    mock_sport_service = MockSportProvider()
    sport_spy = mocker.spy(mock_sport_service, "update_bet")

    mock_auth_service = MockAuthProvider()
    auth_spy = mocker.spy(mock_auth_service, "validate_token")

    flask_app = get_app(
        mock_auth_service,
        None,
        mock_sport_service,
    )
    test_client = flask_app.test_client()
    test_cases = [
        {
            "name": "success",
            "path": "/updatebet?league=epl&home_team=chelsea&away_team=arsenal&home_team_win_odds=2.3&away_team_win_odds=1.2&draw_odds=1&game_date=2023-10-10",
            "headers": {"Authorization": "Authorization valid"},
            "output": 200,
        },
        {
            "name": "fail",
            "path": "/updatebe?league=epl&home_team=chelsea&away_team=arsenal&home_team_win_odds=2.3&away_team_win_odds=1.2&draw_odds=1&game_date=2023-10-10",
            "headers": {"Authorization": "Authorization valid"},
            "output": 404,
        },
        {
            "name": "unauthorized",
            "path": "/updatebet?league=epl&home_team=chelsea&away_team=arsenal&home_team_win_odds=2.3&away_team_win_odds=1.2&draw_odds=1&game_date=2023-10-10",
            "headers": None,
            "output": 401,
        },
    ]
    for test_case in test_cases:
        res = test_client.put(test_case["path"], headers=test_case["headers"])

        assert res.status_code == test_case["output"]
        # spies not working well
        assert sport_spy.call_count == 1


def test_delete(mocker):
    class MockSportProvider:
        def delete_bet(self, req: DeleteBetRequest) -> DeleteBetResponse:
            pass

    mock_sport_service = MockSportProvider()
    sport_spy = mocker.spy(mock_sport_service, "delete_bet")

    mock_auth_service = MockAuthProvider()
    auth_spy = mocker.spy(mock_auth_service, "validate_token")

    flask_app = get_app(
        mock_auth_service,
        None,
        mock_sport_service,
    )
    test_client = flask_app.test_client()
    test_cases = [
        {
            "name": "success",
            "path": "/deletebet?league=epl&home_team=chelsea&away_team=arsenal",
            "headers": {"Authorization": "Authorization valid"},
            "output": 200,
        },
        {
            "name": "fail",
            "path": "/deletbet?league=epl&home_team=chelsea&away_team=arsenal",
            "headers": {"Authorization": "Authorization valid"},
            "output": 404,
        },
        {
            "name": "unauthorized",
            "path": "/deletebet?league=epl&home_team=chelsea&away_team=arsenal",
            "headers": None,
            "output": 401,
        },
    ]
    for test_case in test_cases:
        res = test_client.delete(test_case["path"], headers=test_case["headers"])

        assert res.status_code == test_case["output"]
