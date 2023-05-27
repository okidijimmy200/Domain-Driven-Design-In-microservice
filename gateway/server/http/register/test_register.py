from server.http.server import get_app
from models.user_models import (
    SignUpRequest,
    SignUpResponse,
)


def test_signup(mocker):
    # prepare
    class MockRegistrationProvider:
        def signup(self, req: SignUpRequest):
            return SignUpResponse(200, "OK")

    mock_registration_service = MockRegistrationProvider()
    spy = mocker.spy(mock_registration_service, "signup")

    flask_app = get_app(
        None,
        mock_registration_service,
        None,
    )
    test_client = flask_app.test_client()

    test_cases = [
        {
            "name": "success",
            "path": "/signup",
            "input": {"username": "test", "email": "", "password": ""},
            "output": 200,
        },
    ]
    for test_case in test_cases:
        res = test_client.post(test_case["path"], json=test_case["input"])

        assert res.status_code == test_case["output"]
        # spy.assert_called_once()
