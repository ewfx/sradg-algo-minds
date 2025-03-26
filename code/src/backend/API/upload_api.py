from flask import Blueprint, request, jsonify
import pandas as pd
import os
from valueFeeder import get_anomaly_exists_options, get_anomaly_type_options  

upload_api = Blueprint('upload_api', __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_api.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = os.path.splitext(file.filename)[0]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    file_ext = file.filename.split(".")[-1].lower()
    try:
        if file_ext == "xlsx":
            df = pd.read_excel(filepath)
        elif file_ext == "csv":
            df = pd.read_csv(filepath, encoding="utf-8")
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        df["Match Status"] = get_anomaly_exists_options()
        df["Anomaly Type"] = get_anomaly_type_options()
        df["Comments"] = " "

        modified_filename = f"modified_{filename}.csv"
        modified_filepath = os.path.join(UPLOAD_FOLDER, modified_filename)
        df.to_csv(modified_filepath, index=False, encoding="utf-8")

        return jsonify({
            "message": "File uploaded, converted to CSV, and modified",
            "filename": modified_filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
