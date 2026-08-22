from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the DevOps Kubernetes Project",
        "version": "1.0"
    })


@app.route("/health")
def health():
    return "Application is healthy", 200


@app.route("/api/users")
def users():
    return jsonify([
        {"id": 1, "name": "sunny"},
        {"id": 2, "name": "sandy"},
        {"id": 3, "name": "sony"}
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)