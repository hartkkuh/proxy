from flask import Flask, request, jsonify, Response
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from browser import get_browser

app = Flask(__name__)


@app.route("/open", methods=["GET"])
def open_get():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    browser = get_browser()
    browser.open(url)

    image = browser.img()
    return Response(image, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
