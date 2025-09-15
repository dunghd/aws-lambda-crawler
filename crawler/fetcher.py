import requests
from requests.exceptions import RequestException


def fetch_html(url: str, timeout: int = 10) -> str | None:
    """Fetch HTML content from `url` with a timeout. Returns None on error."""
    headers = {"User-Agent": "aws-lambda-crawler/1.0 (+https://example.com)"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except RequestException:
        return None
