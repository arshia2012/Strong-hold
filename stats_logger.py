from db_connector import DBConnector

connector = DBConnector()


def log_traffic_stats(src_ip, packet_count, distinct_ports, window_seconds):
    connection = connector.get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO traffic_stats (src_ip, packet_count, distinct_ports, window_seconds)
        VALUES (%s, %s, %s, %s)
    """
    values = (src_ip, packet_count, distinct_ports, window_seconds)
    cursor.execute(query, values)


# ============ QUICK TEST ============
if __name__ == "__main__":
    try:
        log_traffic_stats("192.168.1.50", packet_count=12, distinct_ports=3, window_seconds=5.0)
        print(" Traffic stat logged successfully.")
    except Exception as e:
        print(e)