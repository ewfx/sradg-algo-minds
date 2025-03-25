from flask import Flask, request, send_from_directory, jsonify
import pandas as pd
import os
from flask_cors import CORS
from valueFeeder import get_anomaly_exists_options, get_anomaly_type_options  


app = Flask(__name__)

CORS(app) 

# Directory for storing files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# API: Upload Excel/CSV, Convert to CSV, Add Columns
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = os.path.splitext(file.filename)[0]  # Remove extension
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Convert to DataFrame
    file_ext = file.filename.split(".")[-1].lower()
    try:
        if file_ext == "xlsx":
            df = pd.read_excel(filepath)
        elif file_ext == "csv":
            df = pd.read_csv(filepath, encoding="utf-8")
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        # Add two new columns with default value "ABC"
        df["anomaly_exists"] = get_anomaly_exists_options()
        df["anomaly_type"] = get_anomaly_type_options()
        df["Comment"] = " fwfwe "

        # Save as CSV (Ensure all saved files are in CSV format)
        modified_filename = f"modified_{filename}.csv"
        modified_filepath = os.path.join(app.config["UPLOAD_FOLDER"], modified_filename)
        df.to_csv(modified_filepath, index=False, encoding="utf-8")

        return jsonify({
            "message": "File uploaded, converted to CSV, and modified",
            "filename": modified_filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Store updated data
@app.route('/save-updated-data', methods=['POST'])
def save_updated_data():
    data = request.json
    filename = data["filename"]
    table_data = data["tableData"]

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(table_data)
    filepath = f"./processed_files/{filename}"
    df.to_csv(filepath, index=False)

    return jsonify({"message": "Data saved successfully"}), 200

# API: Download the Modified CSV File
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


# API: Get Data as JSON (For React Table)
@app.route("/data/<filename>", methods=["GET"])
def get_data(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    # ✅ Load CSV & Convert to JSON
    df = pd.read_csv(filepath, encoding="utf-8")
    data = df.to_dict(orient="records")  # Convert rows to JSON format
    
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)
