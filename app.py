from flask import Flask, request, jsonify, Response
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from browser import get_browser

app = Flask(__name__)


@app.route("/open", methods=["POST"])
def home():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    browser = get_browser()
    try:
        browser.open(url)
        return jsonify({"success": True})
    except PlaywrightTimeoutError:
        return jsonify({"error": f"Timeout loading {url}"}), 504

@app.route("/img", methods=["GET"])
def img():
    browser = get_browser()
    try:
        image = browser.img()
    except PlaywrightTimeoutError:
        return jsonify({"error": f"Timeout loading image"}), 504
    return Response(image, mimetype="image/png")


@app.route("/click", methods=["POST"])
def click():
    data = request.get_json(silent=True) or {}
    locator = data.get("locator")
    if not locator:
        return jsonify({"error": "Locator is required"}), 400
    browser = get_browser()
    try:
        browser.click(locator, timeout=10000)
    except PlaywrightTimeoutError:
        return jsonify({"error": f"Timeout loading {locator}"}), 504
    return jsonify({"success": True})    

@app.route("/close", methods=["GET"])
def close():
    browser = get_browser()
    try:
        browser.close()
    except PlaywrightTimeoutError:
        return jsonify({"error": f"Timeout closing browser"}), 504
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
