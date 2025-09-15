
import time
import urllib.parse
import urllib.robotparser
from typing import Optional

import requests
from requests.exceptions import RequestException


class RobotsChecker:
    def __init__(self, user_agent: str = "aws-lambda-crawler"):
        self.user_agent = user_agent
        self._parsers: dict[str, urllib.robotparser.RobotFileParser] = {}

    def allowed(self, url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        rp = self._parsers.get(base)
        if rp is None:
            robots_url = urllib.parse.urljoin(base, "/robots.txt")
            rp = urllib.robotparser.RobotFileParser()
            try:
                rp.set_url(robots_url)
                rp.read()
            except Exception:
                # If robots can't be fetched, assume allowed
                rp = None
            self._parsers[base] = rp

        if rp is None:
            return True
        return rp.can_fetch(self.user_agent, url)


def fetch_html(url: str, timeout: int = 10, max_retries: int = 2, backoff: float = 1.0) -> Optional[str]:
    """Fetch HTML content from `url` with robots.txt respect, retries, and timeout.

    Returns HTML text on success or None on error / disallowed by robots.
    """
    headers = {"User-Agent": "aws-lambda-crawler/1.0 (+https://example.com)"}
    rc = RobotsChecker(user_agent=headers["User-Agent"])
    if not rc.allowed(url):
        return None

    attempt = 0
    while attempt <= max_retries:
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except RequestException:
            attempt += 1
            if attempt > max_retries:
                return None
            time.sleep(backoff * attempt)

