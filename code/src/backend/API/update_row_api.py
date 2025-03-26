from flask import Blueprint, request, jsonify
import pandas as pd
import os
from flask_cors import cross_origin

update_row_api = Blueprint('update_row_api', __name__)

UPLOAD_FOLDER = "uploads"

@update_row_api.route('/update-row', methods=['OPTIONS'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def handle_options():
    response = jsonify({"message": "Preflight request allowed"})
    response.status_code = 200
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

@update_row_api.route('/update-row', methods=['POST'])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
def update_row():
    data = request.json
    filename = data["filename"]
    row_index = data["rowIndex"]
    row_data = data["rowData"]

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    df = pd.read_csv(filepath)

    if row_index >= len(df):
        return jsonify({"error": "Invalid row index"}), 400

    for key, value in row_data.items():
        df.at[row_index, key] = value

    df.to_csv(filepath, index=False, encoding="utf-8")

    return jsonify({"message": "Row updated successfully"}), 200
