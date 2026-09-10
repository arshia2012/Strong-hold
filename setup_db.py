"""
One-time setup script for StrongHold's database.
Run this once (python setup_db.py) to create all required tables.
Safe to run multiple times — uses CREATE TABLE IF NOT EXISTS.
"""
from db_connector import DBConnector

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    src_ip VARCHAR(45) NULL,
    severity ENUM('low', 'medium', 'high') NOT NULL DEFAULT 'low',
    details TEXT
);
"""

# Raw periodic traffic snapshots — used to train the ML model.
# Unlike `events`, this table gets a row for EVERY tracked IP on every
# window tick, whether or not it crossed an alert threshold. This is
# what gives the model examples of "normal" behavior to learn from.
CREATE_TRAFFIC_STATS_TABLE = """
CREATE TABLE IF NOT EXISTS traffic_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    src_ip VARCHAR(45) NOT NULL,
    packet_count INT NOT NULL,
    distinct_ports INT NOT NULL,
    window_seconds FLOAT NOT NULL
);
"""

if __name__ == "__main__":
    connector = DBConnector()
    try:
        conn = connector.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(CREATE_EVENTS_TABLE)
            cursor.execute(CREATE_TRAFFIC_STATS_TABLE)
        print(" 'events' and 'traffic_stats' tables are ready.")
    finally:
        connector.close()