from flask import Flask, render_template, request, jsonify
import json
import os
import sys

# Ensure project root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import handler

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/invoke', methods=['POST'])
def invoke():
    url = request.form.get('url')
    payload_text = request.form.get('payload')

    if url:
        event = {'url': url}
    else:
        try:
            event = json.loads(payload_text) if payload_text else {}
        except Exception:
            event = {'body': payload_text}

    try:
        result = handler.lambda_handler(event, None)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

def main() -> None:
    """Entrypoint used by Poetry script `run-webapp`.

    Use `poetry run run-webapp` or `python -m webapp.app`.
    """
    app.run(host='127.0.0.1', port=5000, debug=True)
