import json

def load_anomaly_type_options():
    with open("anomalyType.json","r") as file:
        data = json.load(file)
    return data["anomaly_type_options"]

anomalyExistsOptions = ["Match", "Break"]   
anomalyTypeOptions = load_anomaly_type_options()

def get_anomaly_exists_options():
    return anomalyExistsOptions[0]

def get_anomaly_type_options():
    return anomalyTypeOptions[0]
