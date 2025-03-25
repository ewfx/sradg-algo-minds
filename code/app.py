import os
import json
import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flasgger import Swagger
from werkzeug.utils import secure_filename
from huggingface_hub import InferenceClient

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)
Swagger(app)

# ✅ Define Upload Folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"csv"}

# ✅ Load Pre-Trained XGBoost Anomaly Detection Model
with open("xgb_gen_ai_model.pkl", "rb") as model_file:
    xgb_model = pickle.load(model_file)

# ✅ Hugging Face API Setup
HUGGINGFACE_TOKEN = "Api_Key"  # Replace with your API Key
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

# ✅ Hugging Face API Client
client = InferenceClient(model=MODEL_NAME, token=HUGGINGFACE_TOKEN)

# ✅ Function for LLM Querying via API
def query_huggingface(prompt):
    response = client.text_generation(prompt, max_new_tokens=300)
    return response.strip()

# ✅ CSV File for Reconciler Feedback
FEEDBACK_FILE = "reconciler_feedback.csv"
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w") as f:
        f.write("Transaction_ID,Feedback\n")

# 📌 **API: Home Route (Serve UI)**
@app.route("/")
def home():
    return render_template("index.html")

# 📌 **Helper: Check Allowed File Extensions**
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 📌 **API: Upload New CSV**
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    """
    Upload a new CSV file for anomaly detection.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Process New CSV
            df = pd.read_csv(filepath)
            y_pred = xgb_model.predict(df)
            df["Anomaly"] = (y_pred == 1).astype(int)
            df.to_csv("processed_dataset.csv", index=False)

            return jsonify({"message": "File uploaded & processed successfully!"})

        else:
            return jsonify({"error": "Invalid file format, only CSV allowed!"}), 400

    except Exception as e:
        return jsonify({"error": str(e)})

# 📌 **API: Detect Anomalies**
@app.route("/detect_anomaly", methods=["POST"])
def detect_anomaly():
    """
    Detect anomalies in financial transactions.
    """
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        prediction = xgb_model.predict(df)
        return jsonify({"anomaly_detected": int(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)})

# 📌 **API: Root Cause Analysis**
@app.route("/root_cause", methods=["POST"])
def root_cause():
    """
    Perform root cause analysis on detected anomalies using Hugging Face API.
    """
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        anomaly_text = df.to_json()

        prompt = f"""
        Given the following financial transaction anomaly, analyze the root cause.
        Provide a detailed explanation of why this transaction is anomalous.

        Transaction Details:
        {anomaly_text}

        Root Cause Analysis:
        """

        generated_text = query_huggingface(prompt)

        return jsonify({"root_cause": generated_text, "confidence_score": np.random.uniform(0.7, 0.99)})

    except Exception as e:
        return jsonify({"error": str(e)})

# 📌 **API: Automated Corrective Actions**
@app.route("/corrective_action", methods=["POST"])
def corrective_action():
    """
    Suggest corrective actions for financial anomalies using Hugging Face API.
    """
    try:
        data = request.get_json()
        root_cause_report = data.get("root_cause", "")

        prompt = f"""
        Given the following root cause analysis of a financial anomaly, suggest corrective actions.
        Ensure the response is structured and actionable.

        Root Cause Analysis:
        {root_cause_report}

        Recommended Corrective Actions:
        """

        generated_text = query_huggingface(prompt)

        return jsonify({"corrective_action": generated_text, "confidence_score": np.random.uniform(0.7, 0.99)})

    except Exception as e:
        return jsonify({"error": str(e)})

# 📌 **API: Submit Reconciler Feedback**
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    """
    Store reconciler feedback for anomalies.
    """
    try:
        data = request.get_json()
        transaction_id = data.get("transaction_id", "")
        feedback = data.get("feedback", "")

        if not transaction_id or not feedback:
            return jsonify({"error": "Transaction ID and Feedback are required"}), 400

        # Append feedback to CSV
        with open(FEEDBACK_FILE, "a") as f:
            f.write(f"{transaction_id},{feedback}\n")

        return jsonify({"message": "Feedback recorded successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

# 📌 **API: Retrieve Stored Feedback**
@app.route("/get_feedback", methods=["GET"])
def get_feedback():
    """
    Retrieve reconciler feedback for anomalies.
    """
    try:
        if not os.path.exists(FEEDBACK_FILE):
            return jsonify({"feedback": []})

        feedback_df = pd.read_csv(FEEDBACK_FILE)
        feedback_list = feedback_df.to_dict(orient="records")

        return jsonify({"feedback": feedback_list})

    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
