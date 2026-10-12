# A controlled substitute makes external outcomes repeatable while local
# behavior still runs normally. Patch where the dependency is used. A mock
# specification limits accidental use of methods the real dependency lacks.
#
# Replace only requests.post; keep the real client parsing and validation.

import pytest
import requests
from unittest.mock import patch
from m05.http_client import submit_order
from m08.http_cases import PAYLOAD, response_for


def test_successful_response_is_parsed():
    with patch("m05.http_client.requests.post", return_value=response_for("ok")) as post:
        order = submit_order("http://example.test", PAYLOAD)
    assert order.total_paise == 99800
    post.assert_called_once_with(
        "http://example.test/orders", json=PAYLOAD, timeout=5,
    )


@pytest.mark.parametrize("case, expected_error", [
    ("timeout", requests.Timeout), ("rejected", requests.HTTPError),
    ("malformed", ValueError),
])
def test_external_failures_remain_distinguishable(case, expected_error):
    with patch("m05.http_client.requests.post") as post:
        if case == "timeout":
            post.side_effect = requests.Timeout("Timed out")
        else:
            post.return_value = response_for(case)
        with pytest.raises(expected_error):
            submit_order("http://example.test", PAYLOAD)
# Run: uv run --extra dev pytest m08/s04_external_dependencies.py -q
