from flask import Blueprint, jsonify
import pandas as pd
import os

get_data_api = Blueprint('get_data_api', __name__)

UPLOAD_FOLDER = "uploads"

# API 4: Get Data as JSON (For React Table)
@get_data_api.route("/data/<filename>", methods=["GET"])
def get_data(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    # Load CSV & Convert to JSON
    df = pd.read_csv(filepath, encoding="utf-8")
    data = df.to_dict(orient="records") # Convert rows to JSON format

    return jsonify(data), 200
