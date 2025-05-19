from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'reports.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            timestamp TEXT,
            disk_encryption TEXT,
            os_update TEXT,
            antivirus TEXT,
            sleep_settings TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    required_fields = ["device_id", "disk_encryption", "os_update", "antivirus", "sleep_settings"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    device_id = data["device_id"]
    timestamp = datetime.datetime.now().isoformat()

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO reports (device_id, timestamp, disk_encryption, os_update, antivirus, sleep_settings)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            device_id,
            timestamp,
            data["disk_encryption"],
            data["os_update"],
            data["antivirus"],
            data["sleep_settings"]
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"status": "success", "message": "Report received"}), 200


@app.route('/latest/<device_id>', methods=['GET'])
def get_latest_report(device_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM reports WHERE device_id = ? ORDER BY timestamp DESC LIMIT 1",
        (device_id,)
    )
    row = c.fetchone()
    conn.close()
    if row:
        report = {
            "id": row[0],
            "device_id": row[1],
            "timestamp": row[2],
            "disk_encryption": row[3],
            "os_update": row[4],
            "antivirus": row[5],
            "sleep_settings": row[6]
        }
        return jsonify(report)
    else:
        return jsonify({"error": "No report found for device"}), 404
    
@app.route("/latest-reports", methods=["GET"])
def latest_reports():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Subquery to get latest timestamp per device
    c.execute("""
        SELECT r1.*
        FROM reports r1
        INNER JOIN (
            SELECT device_id, MAX(timestamp) AS max_time
            FROM reports
            GROUP BY device_id
        ) r2
        ON r1.device_id = r2.device_id AND r1.timestamp = r2.max_time
    """)
    rows = c.fetchall()
    conn.close()

    reports = []
    for row in rows:
        reports.append({
            "id": row[0],
            "device_id": row[1],
            "timestamp": row[2],
            "disk_encryption": row[3],
            "os_update": row[4],
            "antivirus": row[5],
            "sleep_settings": row[6]
        })

    return jsonify(reports)

@app.route("/filter", methods=["GET"])
def filter_reports():
    os_update = request.args.get("os_update")
    disk_encryption = request.args.get("disk_encryption")

    query = """
        SELECT r1.*
        FROM reports r1
        INNER JOIN (
            SELECT device_id, MAX(timestamp) AS max_time
            FROM reports
            GROUP BY device_id
        ) r2
        ON r1.device_id = r2.device_id AND r1.timestamp = r2.max_time
        WHERE 1=1
    """
    params = []

    if os_update:
        query += " AND r1.os_update = ?"
        params.append(os_update)

    if disk_encryption:
        query += " AND r1.disk_encryption = ?"
        params.append(disk_encryption)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "device_id": row[1],
            "timestamp": row[2],
            "disk_encryption": row[3],
            "os_update": row[4],
            "antivirus": row[5],
            "sleep_settings": row[6]
        })

    return jsonify(results)

@app.route("/reports", methods=["GET"])
def get_all_latest_reports():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT device_id, MAX(timestamp) as latest_time
        FROM reports
        GROUP BY device_id
    ''')
    latest_times = c.fetchall()

    latest_reports = []
    for device_id, latest_time in latest_times:
        c.execute('''
            SELECT * FROM reports
            WHERE device_id = ? AND timestamp = ?
        ''', (device_id, latest_time))
        row = c.fetchone()
        if row:
            latest_reports.append({
                "id": row[0],
                "device_id": row[1],
                "timestamp": row[2],
                "disk_encryption": row[3],
                "os_update": row[4],
                "antivirus": row[5],
                "sleep_settings": row[6]
            })

    conn.close()
    return jsonify(latest_reports)



if __name__ == "__main__":
    init_db()
    app.run(debug=True)

