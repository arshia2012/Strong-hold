import joblib

def load_model(path='anomaly_model.pkl'):
    model = joblib.load(path)
    return model

def check_anomaly(model, packet_count, distinct_ports):
    
    sample = [[packet_count, distinct_ports]]
    result = model.predict(sample)
    return result[0]


if __name__ == "__main__":
    model = load_model()

    result1 = check_anomaly(model, packet_count=3289, distinct_ports=1000)
    print(f"Kali-like traffic: {'ANOMALY' if result1 == -1 else 'normal'}")

    result2 = check_anomaly(model, packet_count=500, distinct_ports=1)
    print(f"Spotify-like traffic: {'ANOMALY' if result2 == -1 else 'normal'}")

    result3 = check_anomaly(model, packet_count=10, distinct_ports=2)
    print(f"Light traffic: {'ANOMALY' if result3 == -1 else 'normal'}")