from flask import Flask
from flask_restplus import Api

from backend.src.config import ShakuntlaDeviConfig

# Initialising the Flask-App
app = Flask(__name__)
config = ShakuntlaDeviConfig.get_config()
app.config.from_object(config)

# Initialising Flask-RestPLUS
if app.config['DEBUG']:
    api = Api(app)
else:
    api = Api(app, doc=False, specs=False)

# Import all Routes
from backend.src.routes import *
