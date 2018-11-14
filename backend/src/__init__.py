from flask import Flask
from flask_restplus import Api
from flask_cors import CORS

from .config import ShakuntlaDeviConfig

# Initialising the Flask-App
app = Flask(__name__)
CORS(app)
config = ShakuntlaDeviConfig.get_config()
app.config.from_object(config)

# Initialising Flask-RestPLUS
if app.config['DEBUG']:
    api = Api(app)
else:
    api = Api(app, doc=False, specs=False)

# Import all Routes
from .routes import *
