from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

@app.route("/audio", methods=["POST"])
def audio():
    data = request.json
    print("Received:", data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run()
