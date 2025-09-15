from crawler.fetcher import fetch_html
from crawler.parser import parse_html


def lambda_handler(event, context=None):
    """AWS Lambda handler.

    Expects event to be a dict with key `url`.
    Returns a dict with `url`, `title` and `text_snippet`.
    """
    url = event.get("url") if isinstance(event, dict) else None
    if not url:
        return {"error": "missing 'url' in event"}

    html = fetch_html(url)
    if html is None:
        return {"error": "failed to fetch url", "url": url}

    parsed = parse_html(html)
    return {"url": url, **parsed}
