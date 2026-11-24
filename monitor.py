import time
import requests

from enum import Enum



class CheckResult(Enum):
    UP = "up"
    DOWN = "down"
    TIMEOUT = "timeout"


def check_target(url: str, timeout: float) -> tuple[CheckResult, float | None]:
    """Check one URL; return (result, response time in ms, or None if it failed)."""
    start_time = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout)
        response_time = round((time.perf_counter() - start_time) * 1000, 1)
        if response.status_code == response.ok:
            return CheckResult.UP, response_time
        else:
            return CheckResult.DOWN, response_time
    except requests.exceptions.Timeout:
        return CheckResult.TIMEOUT, None
    except requests.exceptions.RequestException:
        return CheckResult.DOWN, None


if __name__ == "__main__":
    print(check_target("https://doesnotexist.invalid", 5))
    print(check_target("http://10.255.255.1", 3))
    print(check_target("https://www.google.com", 5))
