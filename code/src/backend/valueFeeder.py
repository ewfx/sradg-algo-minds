import json
from API.utils.datasetAnalyzer import classify_anomaly_type, anomaly_exists,classify_anomaly


def load_anomaly_type_options():
    with open("anomalyType.json","r") as file:
        data = json.load(file)
    return data["anomaly_type_options"]

anomalyExistsOptions = ["Match", "Break"]   
anomalyTypeOptions = load_anomaly_type_options()



with open("anomalyDescription.json", "r") as file:
    data = json.load(file)

# Function to get anomaly description by category
def get_anomaly_description(category):
    for anomaly in data["anomalies"]:
        if anomaly["category"].lower() == category.lower():  # Case-insensitive match
            return anomaly["description"]
    return " "



data_diff = 0
anomaly_type=""


def get_anomaly_exists_options(row,flag):
    if flag: 
        if abs(row["ihub balance"]-row["gl balance"])>0:
            global data_diff
            data_diff = abs(row["ihub balance"]-row["gl balance"])
            return anomalyExistsOptions[1]
        else:
            return anomalyExistsOptions[0]
    else:
        return anomalyExistsOptions[anomaly_exists()]

def get_anomaly_type_options(row):
    global data_diff
    global anomaly_type
    if data_diff!=0:
        return classify_anomaly_type(row)
    if data_diff==0:
        return anomalyTypeOptions[0]
    


def get_anomaly_type_description(row):
    global anomaly_type
    global data_diff
    if data_diff:
        return get_anomaly_description(anomaly_type)
    else:
        return " "
