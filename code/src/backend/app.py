from flask import Flask
from flask_cors import CORS
from API.upload_api import upload_api
from API.save_data_api import save_data_api
from API.download_api import download_api
from API.get_data_api import get_data_api
from API.update_row_api import update_row_api
from API.send_mail_api import send_mail_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register Blueprints
app.register_blueprint(upload_api)
app.register_blueprint(save_data_api)
app.register_blueprint(download_api)
app.register_blueprint(get_data_api)
app.register_blueprint(update_row_api)
app.register_blueprint(send_mail_bp)

if __name__ == "__main__":
    app.run(debug=True)
