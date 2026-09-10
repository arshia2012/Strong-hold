from db_connector import DBConnector
from sklearn.ensemble import IsolationForest
import joblib
import BetterRich

def fetch_training_data():
    connector = DBConnector()
    connection = connector.get_connection()
    cursor = connection.cursor()

    query = "SELECT packet_count, distinct_ports FROM traffic_stats"
    cursor.execute(query)
    rows = cursor.fetchall()

    features = []
    for row in rows:
        features.append([row['packet_count'], row['distinct_ports']])

    return features

def train_model(features):
    model = IsolationForest(contamination=0.05)
    model.fit(features)
    return model
 
def save_model(model, path='anomaly_model.pkl'):
    joblib.dump(model, path)


if __name__ == "__main__":
    BetterRich.good("Reading database")
    features = fetch_training_data()
    print(f"{len(features)} rows")

    BetterRich.good("training model")
    model = train_model(features)

    save_model(model)
    BetterRich.good("model saved")