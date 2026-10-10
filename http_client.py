"""HTTP helper for JSON API requests."""

from typing import Any

import requests


def get(
    url: str,
    params: dict[str, str] | None = None,
    timeout: int = 10,
) -> Any:
    """Send a GET request, check its status, and return the JSON response."""
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()
