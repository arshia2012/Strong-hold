from db_connector import DBConnector
import BetterRich

connector = DBConnector()

def logInfo(source, event_type, src_ip=None, severity="low", details=""):
    connection = connector.get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO events (source, event_type, src_ip, severity, details)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (source, event_type, src_ip, severity, details)
    cursor.execute(query, values)

if __name__ == "__main__":
    try:
        logInfo("test", "test", "test", "low", "A test")
        BetterRich.good("WORKED")
    except Exception as e:
        BetterRich.warn(e)