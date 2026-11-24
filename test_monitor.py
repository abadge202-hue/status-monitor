import requests

from monitor import CheckResult, check_target


class FakeResponse:
    ok = True


class FakeErrorResponse:
    ok = False


def test_check_target_up(monkeypatch):
    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result, response_time = check_target("https://example.com", 5)

    assert result == CheckResult.UP
    assert response_time is not None


def test_check_target_timeout(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.Timeout()

    monkeypatch.setattr(requests, "get", fake_get)

    result, response_time = check_target("https://example.com", 5)

    assert result == CheckResult.TIMEOUT
    assert response_time is None


def test_check_target_down_connection_error(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, "get", fake_get)

    result, response_time = check_target("https://example.com", 5)

    assert result == CheckResult.DOWN
    assert response_time is None


def test_check_target_down_with_non_ok_response(monkeypatch):
    class FakeErrorResponse:
        ok = False

    def fake_get(url, timeout):
        return FakeErrorResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result, response_time = check_target("https://example.com", 5)

    assert result == CheckResult.DOWN
    assert response_time is not None
