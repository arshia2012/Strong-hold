from flask import Flask, render_template, jsonify
from db_connector import DBConnector

app = Flask(__name__)
connector = DBConnector()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events")
def api_events():
    connection = connector.get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT event_id, timestamp, source, event_type, src_ip, severity, details "
        "FROM events ORDER BY timestamp DESC LIMIT 50"
    )
    rows = cursor.fetchall()
    for row in rows:
        row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(rows)


@app.route("/api/stats")
def api_stats():

    connection = connector.get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM events")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS high FROM events WHERE severity = 'high'")
    high = cursor.fetchone()["high"]

    cursor.execute("SELECT COUNT(DISTINCT src_ip) AS sources FROM events")
    sources = cursor.fetchone()["sources"]

    return jsonify({"total": total, "high": high, "sources": sources})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
