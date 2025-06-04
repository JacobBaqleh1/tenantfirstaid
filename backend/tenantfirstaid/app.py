from pathlib import Path
from flask import Flask, jsonify


if Path(".env").exists():
    from dotenv import load_dotenv

    load_dotenv(override=True)

from .chat import ChatView

from .session import TenantSession

app = Flask(__name__)

session = TenantSession()


@app.get("/api/history/<session_id>")
def history(session_id):
    session_data = session.get(session_id)
    messages = [item for item in session_data if item["type"] == "message"]
    print(f"History for session {session_id}: {messages}")
    return jsonify(messages)


app.add_url_rule(
    "/api/query", view_func=ChatView.as_view("chat", session), methods=["POST"]
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
