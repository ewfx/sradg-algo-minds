from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow import keras
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from pyod.models.hbos import HBOS
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.losses import MeanSquaredError
import requests
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import io  # For handling file uploads

app = Flask(__name__)

# ============== 1. LOAD TRAINED MODELS & SCALER ==============
print("🔄 Loading trained models...")
try:
    models = joblib.load("hybrid_anomaly_model.pkl")
    scaler = joblib.load("scaler.pkl")
except FileNotFoundError as e:
    print(f"❌ Error: Model or scaler file not found: {e}")
    exit()

trained_features = ['form', 'DeviceType', 'TransactionAmt', 'value', 'card1']

mse = MeanSquaredError()
try:
    autoencoder = keras.models.load_model("autoencoder_model.h5", custom_objects={"mse": mse})
    iso_forest = models["iso_forest"]
    lof = models["lof"]
    hbos = models["hbos"]
    threshold = models["threshold"]
except Exception as e:
    print(f"❌ Error loading models: {e}")
    exit()

# ============== 2. LOAD USER-UPLOADED DATA ==============
def load_user_data(file_content):
    try:
        df_user = pd.read_csv(io.StringIO(file_content.decode('utf-8'))) # important change for file upload
        print(f"✅ User dataset loaded: {df_user.shape}")
        return df_user
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None

# ============== 3. FEATURE SELECTION & MAPPING (Enhanced with Gen AI) ==============
def gen_ai_column_mapping(user_columns, trained_features, threshold=0.5):
    # ... (gen_ai_column_mapping function remains the same)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    trained_embeddings = model.encode(trained_features)
    user_embeddings = model.encode(user_columns)

    mapping = {}
    for i, user_col in enumerate(user_columns):
        similarities = cosine_similarity([user_embeddings[i]], trained_embeddings)[0]
        best_match_index = np.argmax(similarities)
        print(f"Similarity of {user_col} to {trained_features[best_match_index]}: {similarities[best_match_index]}")
        if similarities[best_match_index] >= threshold:
            mapping[user_col] = trained_features[best_match_index]
    return mapping

def ensure_column_compatibility(df_user, trained_features):
    # ... (ensure_column_compatibility function remains the same)
    user_columns = df_user.columns.tolist()
    rename_mapping = gen_ai_column_mapping(user_columns, trained_features)
    manual_mapping = {
        "Account": "card1",
        "AU": "DeviceType",
        "GL Balance": "TransactionAmt",
        "iHub Balance": "value",
        "Form Type" : "form"
    }
    rename_mapping.update(manual_mapping)
    df_user = df_user.rename(columns=rename_mapping)
    user_columns = df_user.columns.tolist()
    matching_cols = [col for col in trained_features if col in user_columns]
    if not matching_cols:
        print("⚠️ Renaming failed. Cannot match all required columns.")
        print("Required columns:", trained_features)
        print("Renamed columns:", user_columns)
        return None
    df_user = df_user[matching_cols]
    for col in trained_features:
        if col not in df_user.columns:
            df_user[col] = 0
    df_user = df_user[trained_features]
    print(f"✅ Finalized Feature Set: {df_user.columns.tolist()}")
    return df_user

# ============== 4. PREPROCESS NEW DATA ==============
def preprocess_new_data(file_content, trained_features, scaler):
    df_user = load_user_data(file_content)
    if df_user is None:
        return None
    df_user_numerical = df_user.select_dtypes(include=[np.number])
    df_user_compatible = ensure_column_compatibility(df_user_numerical, trained_features)
    if df_user_compatible is None:
        return None
    try:
        df_user_scaled = scaler.transform(df_user_compatible)
        print("✅ Features scaled successfully.")
        return df_user_scaled
    except ValueError as e:
        print(f"❌ Error during scaling: {e}")
        print("Please ensure your uploaded data's columns match the trained model's required columns.")
        return None

# ============== 5. PREDICT ANOMALIES USING HYBRID MODEL ==============
def predict_anomalies(X):
    autoencoder_scores = np.mean(np.abs(autoencoder.predict(X) - X), axis=1)
    iso_scores = iso_forest.decision_function(X)
    lof_scores = lof.fit_predict(X)
    lof_scores_decision = lof.negative_outlier_factor_
    hbos_scores = hbos.decision_function(X)
    autoencoder_preds = autoencoder_scores > threshold
    iso_preds = iso_scores < 0
    lof_preds = lof_scores == -1
    hbos_preds = hbos_scores > 0
    hybrid_preds = (autoencoder_preds.astype(int) + iso_preds.astype(int) + lof_preds.astype(int) + hbos_preds.astype(int)) >= 2
    return hybrid_preds, autoencoder_scores, iso_scores, lof_scores_decision, hbos_scores

# ============== 6. ROOT CAUSE ANALYSIS USING GEN AI (Hugging Face API) ==============
def analyze_root_cause(row):
    api_token = "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"
    if not api_token:
        print("❌ Error: Hugging Face API token not found in environment variables.")
        return "No insight available"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": f"Analyze the following financial anomaly and explain the potential reasons for it. Consider the relationships between 'form', 'DeviceType', 'TransactionAmt', 'value', and 'card1'. Provide a detailed explanation of why this data might be unusual: {row.to_dict()}"}
    try:
        response = requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during Hugging Face API call: {e}")
        return "No insight available"

# ============== 7. AUTOMATED CORRECTIVE ACTIONS USING GEN AI (Agentic AI) ==============
def suggest_corrective_actions(row, root_cause):
    api_token = "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"
    if not api_token:
        print("❌ Error: Hugging Face API token not found in environment variables.")
        return "No corrective action available"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": f"Given the following anomaly data: {row.to_dict()} and the root cause: {root_cause}, suggest specific and actionable steps to investigate and resolve this anomaly. Consider the potential causes and provide practical recommendations."}
    try:
        response = requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during Hugging Face API call for corrective actions: {e}")
        return "No corrective action available"

# ============== 8. FLASK API AND UI INTEGRATION ==============

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        if file and file.filename.endswith('.csv'):
            file_content = file.read()
            scaled_data = preprocess_new_data(file_content, trained_features, scaler)
            if scaled_data is not None:
                df_user = load_user_data(file_content)
                hybrid_preds, autoencoder_scores, iso_scores, lof_scores_decision, hbos_scores = predict_anomalies(scaled_data)
                df_user["Anomaly"] = hybrid_preds
                df_user["Root_Cause_Analysis"] = df_user.apply(lambda row: analyze_root_cause(row) if row["Anomaly"] else "Normal", axis=1)
                df_user["Corrective_Action"] = df_user.apply(lambda row: suggest_corrective_actions(row, row["Root_Cause_Analysis"]) if row["Anomaly"] else "Normal", axis=1)
                df_user["Autoencoder_Score"] = autoencoder_scores
                df_user["IsolationForest_Score"] = iso_scores
                df_user["LOF_Score"] = lof_scores_decision
                df_user["HBOS_Score"] = hbos_scores

                results = df_user.to_dict(orient='records')
                return render_template('results.html', results=results)
            else:
                return render_template('index.html', error='Preprocessing failed. Please check your CSV file.')
        else:
            return render_template('index.html', error='Invalid file type. Please upload a CSV file.')
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        file_content = file.read()
        scaled_data = preprocess_new_data(file_content, trained_features, scaler)
        if scaled_data is not None:
            df_user = load_user_data(file_content)
            hybrid_preds, autoencoder_scores, iso_scores, lof_scores_decision, hbos_scores = predict_anomalies(scaled_data)
            df_user["Anomaly"] = hybrid_preds
            df_user["Root_Cause_Analysis"] = df_user.apply(lambda row: analyze_root_cause(row) if row["Anomaly"] else "Normal", axis=1)
            df_user["Corrective_Action"] = df_user.apply(lambda row: suggest_corrective_actions(row, row["Root_Cause_Analysis"]) if row["Anomaly"] else "Normal", axis=1)
            df_user["Autoencoder_Score"] = autoencoder_scores
            df_user["IsolationForest_Score"] = iso_scores
            df_user["LOF_Score"] = lof_scores_decision
            df_user["HBOS_Score"] = hbos_scores
            results = df_user.to_dict(orient='records')
            return jsonify({'results': results})
        else:
            return jsonify({'error': 'Preprocessing failed. Please check your CSV file.'}), 400
    else:
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

if __name__ == '__main__':
    app.run(debug=True)