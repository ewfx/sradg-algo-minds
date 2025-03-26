from flask import Blueprint, request, jsonify
import pandas as pd
import os

save_data_api = Blueprint('save_data_api', __name__)

@save_data_api.route('/save-updated-data', methods=['POST'])
def save_updated_data():
    data = request.json
    filename = data["filename"]
    table_data = data["tableData"]

    df = pd.DataFrame(table_data)
    filepath = f"./processed_files/{filename}"
    df.to_csv(filepath, index=False)

    return jsonify({"message": "Data saved successfully"}), 200
