# AWS Lambda HTML Crawler

Minimal project to crawl HTML pages using AWS Lambda (Python).

Features:

- Fetch HTML from a URL
- Parse title and text content
- Lambda handler that accepts `url` in the event

Using Poetry:

1. Install Poetry (if not installed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies and create virtualenv via Poetry:

```bash
poetry install
poetry shell
```

Run locally:

```bash
python local_runner.py https://example.com
```

Deploy:

- Package with dependencies into a zip and upload to AWS Lambda, or use AWS SAM / Serverless Framework.

Run tests:

```bash
poetry run pytest -q
```

Package for AWS Lambda (simple):

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
pip install -r requirements.txt -t package/
cp -r crawler handler.py local_runner.py package/
cd package && zip -r ../deployment.zip .
```
