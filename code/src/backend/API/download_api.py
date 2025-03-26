from flask import Blueprint, send_from_directory
import os

download_api = Blueprint('download_api', __name__)

UPLOAD_FOLDER = "uploads"

# API 3: Download the Modified CSV File
@download_api.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
