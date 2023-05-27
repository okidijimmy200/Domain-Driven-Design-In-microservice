from server.http.server import get_app
from models.user_models import LoginRequest, LoginResponse


def test_login(mocker):
    # prepare
    class MockLoginProvider:
        def login(self, req: LoginRequest):
            return LoginResponse(200, "OK")

    mock_login_service = MockLoginProvider()
    spy = mocker.spy(mock_login_service, "login")

    flask_app = get_app(
        None,
        mock_login_service,
        None,
    )
    test_client = flask_app.test_client()

    test_cases = [
        {
            "name": "success",
            "path": "/login",
            "input": {"email": "", "password": ""},
            "output": 200,
        },
    ]
    for test_case in test_cases:
        res = test_client.post(test_case["path"], json=test_case["input"])

        assert res.status_code == test_case["output"]
        # spy.assert_called_once()
