import pandas as pd
import json
import google.generativeai as genai
import random
def load_anomaly_type_options():
    with open("anomalyType.json","r") as file:
        data = json.load(file)
    return data["anomaly_type_options"]

anomalyTypeOptions = load_anomaly_type_options()

GOOGLE_API_KEY = "AIzaSyCWssAt3t_G0J-QD9I59-4xhLVlHlsP8sQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

with open("anomalyType.json", "r") as f:
    anomaly_types = json.load(f)["anomaly_type_options"]


# Function to generate a dynamic prompt based on the dataset
def generate_prompt(data_row):
    if isinstance(data_row, pd.Series):
        data_row = data_row.to_dict()
    prompt = f"""
    Act as a financial reconciler for a financial institution. Your task is to analyze a given row of financial transaction data and determine the most appropriate anomaly type from the list provided. The row represents a financial transaction that has been flagged as anomalous due to data inconsistencies. Your job is to:

    - **Understand the structure of the data row**: Identify key transaction attributes such as transaction ID, amount, date, account details, currency, and any mismatched values.
    - **Map the anomaly to one of the predefined anomaly types**: Compare the characteristics of the anomaly with the given anomaly types from `anomalyType.json`.
    - **Return at varied reasons** why the anomaly exists.
    - **All reasons must strictly be from the given list of anomaly types**.
    - **DO NOT default to "Unbalanced Accounts" unless it is the most fitting choice. Prioritize other appropriate anomaly types from the list.**
    - **Do NOT say "No anomaly exists"**—there is an anomaly for sure, and it must match one of the predefined types.
    - **Ensure a precise classification**: Consider all available details and determine the best matching anomaly type that describes the issue.
    - **Return only the exact anomaly type as output**: No explanations or additional text should be returned—just the most relevant anomaly type.

    Here are the anomaly types you must choose from:

    {', '.join(anomaly_types)}

    The transaction data is:
    {json.dumps(data_row, indent=4)}

    Carefully map the anomaly to the best matching anomaly type from the list. **Return only the exact anomaly type as output, nothing else.**
    """
    return prompt
def classify_anomaly_type(row):
    return anomalyTypeOptions[random.randint(1, 20)]
def anomaly_exists():
    return random.choice([0, 1])

# Function to get AI-generated column selection
def classify_anomaly(row):
    global model
    prompt = generate_prompt(row)
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else "No classification found"

