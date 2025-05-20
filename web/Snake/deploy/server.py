from flask import Flask, request, jsonify, render_template
import time
import hmac
import hashlib
import os

app = Flask(__name__, static_folder='static')
SECRET_KEY = b'super_secret_key'

def verify_token(score, timestamp, token):
    msg = f"{score}:{timestamp}".encode()
    expected = hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, token)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/get_flag', methods=['POST'])
def get_flag():
    data = request.json
    score = data.get("score")
    timestamp = data.get("timestamp")
    token = data.get("token")

    if not (score and timestamp and token):
        return jsonify({"error": "Invalid request"}), 400

    if abs(time.time() - timestamp) > 10:
        return jsonify({"error": "Too slow"}), 403

    if score == 1000 and verify_token(score, timestamp, token):
        return jsonify({"flag": "goctf{sn@k3_13g1t_ch3ck}"})
    return jsonify({"error": "No flag for you"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
